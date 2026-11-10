
import csv
import os
import uuid
from pathlib import Path

from google.cloud import bigquery

from src.transform import transform_sale


def read_sales_csv(file_path: Path) -> list[dict]:
    """Read and validate all sales records from the CSV file."""

    transformed_records = []

    with file_path.open(
        mode="r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        reader = csv.DictReader(file)

        # Remove invisible BOM characters and surrounding spaces
        if reader.fieldnames:
            reader.fieldnames = [
                field.strip().lstrip("\ufeff")
                for field in reader.fieldnames
            ]

        print(f"Detected CSV headers: {reader.fieldnames!r}")

        expected_fields = {
            "order_id",
            "order_date",
            "product",
            "quantity",
            "unit_price",
        }

        if not reader.fieldnames or set(reader.fieldnames) != expected_fields:
            raise ValueError("CSV headers do not match the expected schema.")

        seen_order_ids = set()

        for row_number, record in enumerate(reader, start=2):
            try:
                transformed = transform_sale(record)
            except ValueError as error:
                raise ValueError(
                    f"Invalid record on CSV row {row_number}: {error}"
                ) from error

            order_id = transformed["order_id"]

            if order_id in seen_order_ids:
                raise ValueError(
                    f"Duplicate order_id {order_id} on CSV row {row_number}."
                )

            seen_order_ids.add(order_id)
            transformed_records.append(transformed)

    if not transformed_records:
        raise ValueError("The sales CSV contains no records.")

    return transformed_records


def load_to_bigquery(records: list[dict]) -> None:
    """Stage sales records and merge them into the destination table."""

    project_id = os.environ["GCP_PROJECT_ID"]
    dataset_id = os.environ.get("BQ_DATASET", "sales_cicd")
    table_id = os.environ.get("BQ_TABLE", "sales_raw")

    destination = f"{project_id}.{dataset_id}.{table_id}"
    staging_id = f"_staging_sales_{uuid.uuid4().hex}"
    staging = f"{project_id}.{dataset_id}.{staging_id}"

    client = bigquery.Client(project=project_id)

    schema = [
        bigquery.SchemaField("order_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("order_date", "DATE", mode="REQUIRED"),
        bigquery.SchemaField("product", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("quantity", "INT64", mode="REQUIRED"),
        bigquery.SchemaField("unit_price", "NUMERIC", mode="REQUIRED"),
    ]

    load_config = bigquery.LoadJobConfig(
        schema=schema,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    try:
        load_job = client.load_table_from_json(
            records,
            staging,
            job_config=load_config,
        )
        load_job.result()

        merge_sql = f"""
            MERGE `{destination}` AS target
            USING `{staging}` AS source
            ON target.order_id = source.order_id

            WHEN MATCHED THEN
                UPDATE SET
                    order_date = source.order_date,
                    product = source.product,
                    quantity = source.quantity,
                    unit_price = source.unit_price

            WHEN NOT MATCHED THEN
                INSERT (
                    order_id,
                    order_date,
                    product,
                    quantity,
                    unit_price
                )
                VALUES (
                    source.order_id,
                    source.order_date,
                    source.product,
                    source.quantity,
                    source.unit_price
                )
        """


        merge_job = client.query(merge_sql)

        try:
            merge_job.result()
        
        except Exception as error:
            print("BIGQUERY MERGE ERROR:")
            print(repr(error))
            print(f"JOB ID: {merge_job.job_id}")
            print(f"ERROR RESULT: {merge_job.error_result}")
            print(f"ALL ERRORS: {merge_job.errors}")
            raise

        
        print(
            f"Successfully merged {len(records)} records into {destination}."
        )

    finally:
        client.delete_table(staging, not_found_ok=True)


def main() -> None:
    """Execute the sales ETL pipeline."""

    csv_path = Path(__file__).parent / "data" / "sales.csv"

    print("Starting sales ETL pipeline...")

    records = read_sales_csv(csv_path)

    print(f"Validated {len(records)} sales records.")

    load_to_bigquery(records)

    print("Sales ETL pipeline completed successfully.")


if __name__ == "__main__":
    main()
