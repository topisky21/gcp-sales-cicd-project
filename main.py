
import csv
import os
from pathlib import Path

from google.cloud import bigquery

from src.transform import transform_sale


def read_sales_csv(file_path: Path) -> list[dict]:
    """Read and transform all sales records from the CSV file."""

    transformed_records = []

    with file_path.open(mode="r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        expected_fields = {
            "order_id",
            "order_date",
            "product",
            "quantity",
            "unit_price",
        }

        if not reader.fieldnames or set(reader.fieldnames) != expected_fields:
            raise ValueError(
                "CSV headers do not match the expected sales schema."
            )

        for row_number, record in enumerate(reader, start=2):
            try:
                transformed_records.append(transform_sale(record))
            except ValueError as error:
                raise ValueError(
                    f"Invalid record on CSV row {row_number}: {error}"
                ) from error

    if not transformed_records:
        raise ValueError("The sales CSV contains no records.")

    return transformed_records


def load_to_bigquery(records: list[dict]) -> None:
    """Load transformed sales records into BigQuery."""

    project_id = os.environ["project-09a7fa74-88ba-427a-b50"]
    dataset_id = os.environ.get("BQ_DATASET", "sales_cicd")
    table_id = os.environ.get("BQ_TABLE", "sales_raw")

    destination = f"{project_id}.{dataset_id}.{table_id}"

    client = bigquery.Client(project=project_id)

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    )

    job = client.load_table_from_json(
        records,
        destination,
        job_config=job_config,
    )

    job.result()

    print(f"Successfully loaded {len(records)} records into {destination}.")


def main() -> None:
    """Run the sales ETL pipeline."""

    csv_path = Path(__file__).parent / "data" / "sales.csv"

    print("Starting sales ETL pipeline...")

    records = read_sales_csv(csv_path)

    print(f"Successfully validated {len(records)} sales records.")

    load_to_bigquery(records)

    print("Sales ETL pipeline completed successfully.")


if __name__ == "__main__":
    main()
