
# GCP Sales ETL CI/CD Pipeline
## Building an Automated Serverless Data Engineering Pipeline with Google Cloud Platform

![Google Cloud](https://img.shields.io/badge/Google%20Cloud-GCP-4285F4?logo=googlecloud&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![BigQuery](https://img.shields.io/badge/BigQuery-Data%20Warehouse-669DF6?logo=googlebigquery&logoColor=white)
![Cloud Run](https://img.shields.io/badge/Cloud%20Run-Jobs-4285F4?logo=googlecloud&logoColor=white)
![Cloud Build](https://img.shields.io/badge/CI%2FCD-Cloud%20Build-34A853?logo=googlecloud&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-Version%20Control-181717?logo=github&logoColor=white)

---

## Table of Contents

1. [Project Overview](#1-Project-Overview)
2. [Business Problem](#2-business-problem)
3. [Project Objectives](#3-project-objectives)
4. [Solution Architecture](#4-solution-architecture)
5. [Technology Stack](#5-technology-stack)
6. [Google Cloud Infrastructure](#6-google-cloud-infrastructure)
7. [Repository Structure](#7-repository-structure)
8. [ETL Pipeline Implementation](#8-etl-pipeline-implementation)
9. [Data Quality and Validation](#9-data-quality-and-validation)
10. [BigQuery Data Warehouse Design](#10-bigquery-data-warehouse-design)
11. [SQL MERGE and Data Management](#11-sql-merge-and-data-management)
12. [CI/CD Implementation](#12-cicd-implementation)
13. [Cloud Run Jobs and Serverless Execution](#13-cloud-run-jobs-and-serverless-execution)
14. [IAM and Security Architecture](#14-iam-and-security-architecture)
15. [Automated Testing](#15-automated-testing)
16. [Deployment Process](#16-deployment-process)
17. [Technical Challenges and Resolutions](#17-technical-challenges-and-resolutions)
18. [Troubleshooting and Lessons Learned](#18-troubleshooting-and-lessons-learned)
19. [Skills Demonstrated](#19-skills-demonstrated)
20. [Testing and Verification](#20-testing-and-verification)
21. [Business and Engineering Value](#21-business-and-engineering-value)
22. [Future Improvements](#22-future-improvements)
23. [Project Outcome](#23-project-outcome)
24. [Repository](#24-repository)
25. [Author](#25-author)

---

# 1. Project Overview

This project demonstrates the design, development, deployment and execution of an automated, serverless sales data engineering pipeline using Google Cloud Platform (GCP).

The solution automates the extraction of sales records from a CSV file, validates and transforms the data using Python, and loads the processed records into Google BigQuery.

The project incorporates a Continuous Integration and Continuous Deployment (CI/CD) workflow using GitHub and Google Cloud Build. The objective was to establish an automated development and build process that reduces manual deployment activities and provides a repeatable approach to application delivery.

The application is deployed as a Google Cloud Run Job, which executes the ETL workload without requiring a continuously running application server.

The pipeline uses a temporary BigQuery staging table and a SQL `MERGE` operation to insert new sales records and update existing records based on their business key, `order_id`.

The project was deliberately implemented without manually creating or maintaining a Dockerfile. Google Cloud Buildpacks handles application image creation as part of the build process.

This provides practical experience across several areas of cloud engineering:

- Cloud infrastructure and resource configuration.
- Python-based ETL development.
- Data quality and validation.
- BigQuery data warehouse integration.
- SQL-based data management.
- CI/CD automation.
- Serverless batch processing.
- Container image management.
- IAM and service account security.
- Cloud application troubleshooting.

The project was designed as a practical portfolio implementation to demonstrate how individual cloud services can be integrated into a working data engineering solution.

## Project Summary

| Area | Implementation |
|---|---|
| Project type | Cloud-based batch ETL pipeline |
| Cloud provider | Google Cloud Platform |
| Programming language | Python |
| Source data | CSV |
| Data warehouse | Google BigQuery |
| Build automation | Google Cloud Build |
| Source control | GitHub |
| Container image creation | Google Cloud Buildpacks |
| Image repository | Artifact Registry |
| Application execution | Cloud Run Jobs |
| Data processing | Python and SQL |
| Testing | Python unittest |
| Infrastructure security | IAM and dedicated service accounts |
| Deployment region | `europe-west2` |

---

# 2. Business Problem

Organisations regularly receive operational data from different systems in formats such as CSV files.

Sales information, for example, may be exported from point-of-sale systems, customer management platforms, financial applications or internal operational databases.

Before this information can be used for reporting and analytics, it must be extracted, validated, transformed and loaded into a central data warehouse.

A manually managed process can introduce several problems:

- Inconsistent data formats between source files.
- Missing or incorrectly formatted business fields.
- Duplicate business records.
- Invalid dates and numerical values.
- Incompatible source and destination data types.
- Manual application deployment.
- Limited repeatability.
- Difficulty identifying the cause of pipeline failures.
- Inconsistent access permissions across cloud resources.

These issues can affect data quality, reporting accuracy and operational efficiency.

### Proposed Solution

I developed an automated ETL pipeline that:

1. Reads sales data from a CSV source.
2. Validates the input structure.
3. Checks individual records against defined business rules.
4. Transforms valid records into a consistent data structure.
5. Loads records into a temporary BigQuery staging table.
6. Executes a SQL MERGE operation against the destination table.
7. Removes the temporary staging table after processing.

The application is deployed through a CI/CD workflow using GitHub and Cloud Build.

This approach separates application development, testing, image creation, deployment and execution into manageable stages.

---

# 3. Project Objectives

The project was developed around the following engineering objectives.

### Data Engineering Objectives

- Develop a modular Python ETL application.
- Extract structured data from CSV files.
- Implement reusable data validation functions.
- Apply consistent data transformation rules.
- Integrate Python with BigQuery.
- Implement staging and destination table processing.
- Use SQL MERGE to manage new and existing records.

### Cloud Engineering Objectives

- Provision and configure GCP resources.
- Configure Artifact Registry.
- Create dedicated service accounts.
- Configure IAM permissions.
- Deploy a batch application using Cloud Run Jobs.
- Integrate cloud services through service account authentication.

### DevOps and CI/CD Objectives

- Maintain application code in GitHub.
- Connect GitHub to Cloud Build.
- Configure automated build triggers.
- Run unit tests during the build process.
- Build application images using Cloud Buildpacks.
- Publish images to Artifact Registry.
- Deploy the application to Cloud Run Jobs.

### Security Objectives

- Separate build and runtime identities.
- Apply least-privilege IAM permissions.
- Avoid unnecessary project-wide access.
- Restrict Artifact Registry permissions to the required repository.
- Grant BigQuery data permissions at dataset level.

---

# 4. Solution Architecture

The solution follows a serverless batch-processing architecture.

## 4.1 High-Level Architecture

```text
                       DEVELOPER
                           |
                           |
                    GitHub Repository
                           |
                           |
                  Push to Main Branch
                           |
                           |
                 Cloud Build Trigger
                           |
                           |
                  Source Code Retrieval
                           |
                           |
                  Automated Unit Tests
                           |
                           |
                Google Cloud Buildpacks
                           |
                           |
                    Artifact Registry
                           |
                           |
                    Cloud Run Job
                           |
                           |
                 Python ETL Application
                           |
                           |
                  Extract Sales CSV
                           |
                           |
                   Validate Records
                           |
                           |
                 Transform Sales Data
                           |
                           |
                BigQuery Staging Table
                           |
                           |
                      SQL MERGE
                           |
                           |
                BigQuery Destination
                           |
                           |
                sales_cicd.sales_raw
```

## 4.2 Architecture Component Responsibilities

| Component | Responsibility |
|---|---|
| Developer | Maintains application code |
| GitHub | Stores source code and tracks changes |
| Cloud Build Trigger | Detects changes to the configured branch |
| Cloud Build | Executes the automated build workflow |
| Python unittest | Validates transformation logic |
| Cloud Buildpacks | Builds the application container image |
| Artifact Registry | Stores the built application image |
| Cloud Run Jobs | Executes the batch-processing workload |
| Python ETL application | Extracts, validates and loads sales records |
| BigQuery staging table | Temporarily stores validated records |
| SQL MERGE | Updates existing records and inserts new records |
| BigQuery destination | Stores the processed sales data |
| IAM | Controls access between resources |

## 4.3 Architectural Design Decisions

### Why Cloud Run Jobs?

The workload is a finite batch-processing operation.

It does not need to maintain a continuously running HTTP endpoint or respond to individual application requests.

Cloud Run Jobs are therefore appropriate because they execute a defined task and terminate when processing is complete.

### Why BigQuery?

BigQuery provides a managed analytical data warehouse that supports SQL-based processing and integration with Python applications.

It removes the need to manage the underlying database infrastructure.

### Why Artifact Registry?

Artifact Registry provides a central repository for storing the application image produced by Cloud Build.

This separates image creation from application execution.

### Why Cloud Buildpacks?

Buildpacks were used to build the application image without manually creating a Dockerfile.

This reduced the amount of container configuration required while retaining the benefits of container-based deployment.

---

# 5. Technology Stack

| Technology | Purpose | Skills Demonstrated |
|---|---|---|
| Python | ETL application development | Programming and data processing |
| CSV | Source data ingestion | Structured file processing |
| Google Cloud Platform | Cloud infrastructure | Cloud engineering |
| GitHub | Source control | Version management |
| Cloud Build | Build automation | CI/CD |
| Cloud Build Trigger | Automated build initiation | Event-driven automation |
| Cloud Buildpacks | Application image creation | Containerisation concepts |
| Artifact Registry | Image storage | Container registry management |
| Cloud Run Jobs | Batch application execution | Serverless computing |
| BigQuery | Data warehouse | Cloud data engineering |
| SQL | Data manipulation | Data modelling and query development |
| Python unittest | Application testing | Software quality assurance |
| IAM | Access management | Cloud security |
| Service Accounts | Workload identity | Secure service authentication |

---

# 6. Google Cloud Infrastructure

The solution was implemented in the Google Cloud London region.

## 6.1 Project Configuration

| Configuration | Value |
|---|---|
| Cloud provider | Google Cloud Platform |
| Project ID | `project-09a7fa74-88ba-427a-b50` |
| Region | `europe-west2` |
| GitHub username | `topisky21` |
| Repository | `TOPISKY21-GCP-SALES-CICD-PROJECT` |

## 6.2 Cloud Resources Created

| Resource | Name | Purpose |
|---|---|---|
| Artifact Registry | `sales-etl-repo` | Stores application images |
| Cloud Build connection | `github-connection` | Connects GitHub to GCP |
| Cloud Build trigger | `sales-etl-github-trigger` | Automates builds |
| Cloud Run Job | `sales-etl-job` | Executes ETL workload |
| BigQuery dataset | `sales_cicd` | Stores sales data |
| BigQuery table | `sales_raw` | Destination table |
| Runtime service account | `sales-etl-runtime` | Executes the ETL application |
| Build service account | `sales-etl-build` | Performs build and deployment activities |

## 6.3 Regional Configuration

The primary resources were configured in:

```text
europe-west2
```

Using a consistent region simplifies resource management and reduces unnecessary cross-region dependencies.

---

# 7. Repository Structure

The project repository was organised to separate application logic, data, tests and deployment configuration.

```text
TOPISKY21-GCP-SALES-CICD-PROJECT/
│
├── data/
│   └── sales.csv
│
├── src/
│   ├── __init__.py
│   └── transform.py
│
├── tests/
│   └── test_transform.py
│
├── main.py
├── requirements.txt
├── cloudbuild.yaml
├── README.md
└── .gitignore
```

## 7.1 File Responsibilities

| File | Description |
|---|---|
| `main.py` | Application entry point and ETL orchestration |
| `src/__init__.py` | Marks the source directory as a Python package |
| `src/transform.py` | Contains reusable data validation and transformation logic |
| `tests/test_transform.py` | Contains automated unit tests |
| `data/sales.csv` | Sample sales source dataset |
| `requirements.txt` | Defines Python dependencies |
| `cloudbuild.yaml` | Defines the Cloud Build workflow |
| `.gitignore` | Excludes unnecessary files from source control |
| `README.md` | Documents the architecture and implementation |

## 7.2 Modular Application Design

The application separates transformation logic from pipeline orchestration.

`src/transform.py` handles the validation and normalisation of individual sales records.

`main.py` manages:

- CSV extraction.
- Record processing.
- BigQuery connectivity.
- Staging table creation.
- Data loading.
- SQL MERGE execution.
- Temporary table cleanup.

This separation makes the application easier to maintain and test.

It also allows the transformation logic to be reused independently of the cloud infrastructure.

---

# 8. ETL Pipeline Implementation

The ETL application consists of three main stages:

1. Extraction.
2. Transformation.
3. Loading.

## 8.1 Extraction

The application reads sales records from:

```text
data/sales.csv
```

The source dataset contains the following fields:

```csv
order_id,order_date,product,quantity,unit_price
ORD-001,2026-11-01,Laptop,2,750.50
ORD-002,2026-11-02,Monitor,3,180.00
ORD-003,2026-11-03,Keyboard,5,45.99
ORD-004,2026-11-04,Mouse,10,19.50
ORD-005,2026-11-05,Headphones,4,65.75
```

The extraction process uses Python's built-in `csv` module.

The application reads the file using:

```python
with file_path.open(
    mode="r",
    encoding="utf-8-sig",
    newline=""
) as file:
    reader = csv.DictReader(file)
```

Using `utf-8-sig` helps handle CSV files containing a UTF-8 byte-order mark.

The application also normalises the column headers before validating the source structure.

```python
reader.fieldnames = [
    field.strip().lstrip("\ufeff")
    for field in reader.fieldnames
]
```

This prevents invisible characters and unnecessary whitespace from causing header validation failures.

### Extraction Controls

The extraction stage checks that:

- The file can be opened.
- The expected column headers exist.
- The source contains records.
- Individual records can be processed.
- Duplicate order IDs are not present in the same input file.

## 8.2 Transformation

The transformation logic is implemented in:

```text
src/transform.py
```

The function:

```python
transform_sale(record: dict) -> dict
```

validates and normalises each incoming sales record.

The transformation process uses Python data structures and the `Decimal` module to validate numerical values.

### Data Transformation Rules

| Field | Transformation or validation |
|---|---|
| `order_id` | Checks presence and removes surrounding whitespace |
| `order_date` | Validates ISO date format |
| `product` | Checks presence and removes surrounding whitespace |
| `quantity` | Validates positive whole-number values |
| `unit_price` | Validates finite, non-negative decimal values |

### Why Use Decimal?

Financial values should not rely on binary floating-point arithmetic when precision matters.

The Python `Decimal` type provides decimal-based arithmetic and validation.

This is particularly useful when processing monetary fields such as unit prices.

### Validation Behaviour

The application rejects:

- Missing required fields.
- Null values.
- Empty order IDs.
- Empty product descriptions.
- Invalid date values.
- Zero or negative quantities.
- Decimal quantities.
- Negative unit prices.
- Non-finite numerical values.
- Monetary values outside the supported BigQuery NUMERIC range.
- Values with unsupported decimal precision.

The transformation function returns a normalised record suitable for loading into BigQuery.

## 8.3 Loading

The loading stage is implemented in `main.py`.

The application uses the Google Cloud BigQuery Python client:

```python
from google.cloud import bigquery
```

The client is initialised using the project ID:

```python
client = bigquery.Client(project=project_id)
```

The application uses the Cloud Run runtime service account for authentication rather than storing service account credentials in the source code.

### Loading Process

The process follows these steps:

1. Retrieve the GCP project ID from the environment.
2. Identify the BigQuery dataset and destination table.
3. Generate a unique staging table name.
4. Define the expected BigQuery schema.
5. Load the transformed records into the staging table.
6. Wait for the load job to complete.
7. Execute the SQL MERGE operation.
8. Wait for the MERGE job to complete.
9. Delete the temporary staging table.

### Environment Variables

The application uses:

| Variable | Purpose |
|---|---|
| `GCP_PROJECT_ID` | Identifies the GCP project |
| `BQ_DATASET` | Defines the destination dataset |
| `BQ_TABLE` | Defines the destination table |

The dataset and table variables have application defaults where configured.

---

# 9. Data Quality and Validation

Data quality is an important part of the pipeline.

Rather than allowing unvalidated source records to enter the warehouse, the application applies validation rules before loading.

## 9.1 Required Field Validation

The application expects the following fields:

```text
order_id
order_date
product
quantity
unit_price
```

The application checks that the CSV headers match the expected structure.

This prevents unexpected source-file changes from silently producing incorrect results.

## 9.2 Duplicate Record Detection

The application maintains a set of order IDs encountered during CSV processing.

```python
seen_order_ids = set()
```

Before adding a record to the transformed dataset, the application checks whether the order ID has already appeared.

Duplicate records within the same source file are rejected.

## 9.3 Date Validation

The application uses:

```python
date.fromisoformat()
```

This validates the incoming date against the expected ISO date format.

For example:

```text
2026-11-01
```

## 9.4 Quantity Validation

Quantity must be:

- Present.
- Numeric.
- Finite.
- A whole number.
- Greater than zero.

## 9.5 Monetary Validation

The `unit_price` field is validated using Python's `Decimal` functionality.

The validation checks that the value is finite, non-negative and within the supported precision and range.

This helps prevent invalid monetary values from being passed to BigQuery.

## 9.6 Error Reporting

When a record fails validation, the application includes the CSV row number in the error message.

For example:

```python
raise ValueError(
    f"Invalid record on CSV row {row_number}: {error}"
)
```

This makes it easier to identify the source of a data-quality problem.

---

# 10. BigQuery Data Warehouse Design

BigQuery was selected as the destination analytical warehouse.

The dataset created for the project is:

```text
sales_cicd
```

The destination table is:

```text
sales_raw
```

The fully qualified table name is:

```text
project-09a7fa74-88ba-427a-b50.sales_cicd.sales_raw
```

## 10.1 Destination Schema

| Column | BigQuery Data Type | Mode | Description |
|---|---|---|---|
| `order_id` | STRING | REQUIRED | Unique business identifier |
| `order_date` | DATE | REQUIRED | Date of the sales transaction |
| `product` | STRING | REQUIRED | Product description |
| `quantity` | INT64 | REQUIRED | Number of units sold |
| `unit_price` | NUMERIC | REQUIRED | Unit selling price |

## 10.2 Schema Design Considerations

The schema uses explicit data types rather than relying on automatic type detection.

This is important because source files can contain values that BigQuery might otherwise infer inconsistently.

The selected data types provide:

- `STRING` for business identifiers and product descriptions.
- `DATE` for transaction dates.
- `INT64` for whole-number quantities.
- `NUMERIC` for monetary values.

The Python application defines the same schema when creating the staging table.

Maintaining consistency between the application schema and the destination schema is essential to successful data loading.

---

# 11. SQL MERGE and Data Management

The pipeline uses a staging-and-MERGE pattern.

This is a common approach when processing batch data that may contain both new and previously loaded business records.

## 11.1 Why Use Staging?

The staging table acts as an intermediate processing layer.

It allows the application to load and validate a batch before applying changes to the destination table.

The staging table is generated dynamically:

```python
staging_id = f"_staging_sales_{uuid.uuid4().hex}"
```

This creates a unique name for each execution.

The staging table identifier includes the project and dataset:

```python
staging = f"{project_id}.{dataset_id}.{staging_id}"
```

This ensures that the table is referenced using its fully qualified BigQuery identifier.

## 11.2 MERGE Logic

The SQL MERGE operation uses `order_id` as the matching key.

```sql
MERGE `project_id.sales_cicd.sales_raw` AS target
USING `project_id.sales_cicd.staging_table` AS source
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
    );
```

### When a Record Matches

If the incoming `order_id` already exists in the destination table, the existing record is updated.

### When a Record Does Not Match

If the incoming `order_id` does not exist, a new record is inserted.

### Temporary Table Cleanup

The application uses a `finally` block:

```python
finally:
    client.delete_table(staging, not_found_ok=True)
```

This ensures that the temporary staging table is cleaned up after the loading and MERGE processing attempt.

## 11.3 Idempotency Considerations

The MERGE operation is designed to support repeatable processing based on the order ID.

However, a formal idempotency acceptance test should be completed before claiming that repeated executions have been verified.

The acceptance test should:

1. Execute the Cloud Run Job.
2. Confirm the destination record count.
3. Execute the same job again.
4. Confirm that the destination record count remains unchanged.
5. Confirm that no duplicate order IDs exist.

This is an important distinction between implementing MERGE logic and formally testing end-to-end idempotency.

---

# 12. CI/CD Implementation

The project uses GitHub and Google Cloud Build to automate the application build process.

The purpose of this implementation was to reduce manual build activities and establish a repeatable development workflow.

## 12.1 GitHub Integration

The source code is maintained in:

```text
TOPISKY21-GCP-SALES-CICD-PROJECT
```

Repository:

https://github.com/topisky21/TOPISKY21-GCP-SALES-CICD-PROJECT

A second-generation Cloud Build connection was created:

```text
github-connection
```

The GitHub repository was connected successfully.

## 12.2 Cloud Build Trigger

The Cloud Build trigger is:

```text
sales-etl-github-trigger
```

The trigger is configured to monitor:

```text
^main$
```

This means that the configured build workflow is initiated when changes are pushed to the main branch.

The build configuration file is:

```text
cloudbuild.yaml
```

## 12.3 Build Workflow

The workflow consists of the following stages:

### Stage 1: Source Retrieval

Cloud Build retrieves the latest source code from the connected GitHub repository.

### Stage 2: Automated Testing

The build process executes:

```bash
python -m unittest discover -s tests -v
```

This checks the transformation logic before the application image is built.

### Stage 3: Application Image Creation

Google Cloud Buildpacks detects the Python application and builds the container image.

A manually maintained Dockerfile is not required for this implementation.

### Stage 4: Image Publication

The generated image is pushed to:

```text
sales-etl-repo
```

in Artifact Registry.

### Stage 5: Deployment Configuration

The Cloud Run Job is configured to use the application image.

The deployed job is:

```text
sales-etl-job
```

## 12.4 Benefits of the CI/CD Implementation

- Reduces manual build activities.
- Provides a repeatable build process.
- Integrates automated tests into the delivery workflow.
- Maintains source control through GitHub.
- Stores application images centrally.
- Separates application build and execution.
- Provides a foundation for controlled deployment environments.

---

# 13. Cloud Run Jobs and Serverless Execution

Cloud Run Jobs were selected as the execution environment for the ETL application.

Unlike a continuously running Cloud Run service, a Cloud Run Job executes a task and terminates when the task completes.

This matches the requirements of a batch ETL workload.

## 13.1 Cloud Run Job Configuration

The deployed job is:

```text
sales-etl-job
```

The job executes the Python application using the image published to Artifact Registry.

The runtime identity is:

```text
sales-etl-runtime@project-09a7fa74-88ba-427a-b50.iam.gserviceaccount.com
```

## 13.2 Runtime Process

During execution:

1. Cloud Run starts the configured application container.
2. Python loads the application.
3. The CSV file is read.
4. Sales records are validated.
5. Records are transformed.
6. The application connects to BigQuery.
7. A temporary staging table is populated.
8. The MERGE operation updates the destination.
9. The staging table is deleted.
10. The application terminates successfully.

## 13.3 Why Serverless Execution?

The serverless model reduces the need to manage virtual machines, operating system maintenance and continuously running application infrastructure.

It is particularly suitable for workloads that run periodically or on demand.

Potential future extensions include scheduled execution using Cloud Scheduler.

---

# 14. IAM and Security Architecture

Security was considered during the infrastructure configuration.

Separate service accounts were created for build and runtime activities.

This avoids relying on a single identity with broad permissions across the entire solution.

## 14.1 Build Service Account

Identity:

```text
sales-etl-build@project-09a7fa74-88ba-427a-b50.iam.gserviceaccount.com
```

The build service account was configured with permissions required for:

- Cloud Build operations.
- Artifact Registry image publication.
- Cloud Run deployment activities.
- Build logging.
- Acting as the designated runtime service account where required.

### Artifact Registry Permissions

Artifact Registry Writer was assigned at the repository level:

```text
sales-etl-repo
```

The broader project-level Artifact Registry Writer grant was removed after the repository-level permission had been verified.

This reduced the scope of the build identity's access.

## 14.2 Runtime Service Account

Identity:

```text
sales-etl-runtime@project-09a7fa74-88ba-427a-b50.iam.gserviceaccount.com
```

The runtime identity received:

| IAM Role | Scope | Purpose |
|---|---|---|
| BigQuery Job User | Project | Allows BigQuery job execution |
| BigQuery Data Editor | `sales_cicd` dataset | Allows the application to manage data in the relevant dataset |

This allows the application to interact with BigQuery without requiring unrestricted access to all project datasets.

## 14.3 Least-Privilege Security

The implementation demonstrates several security principles:

- Separate identities for build and runtime operations.
- Dataset-level permissions for data access.
- Repository-level Artifact Registry permissions.
- Removal of unnecessary broader permissions.
- Service account authentication.
- Avoidance of hard-coded service account keys.

## 14.4 Secret Manager

The Secret Manager API was enabled during the infrastructure setup.

The current sample ETL implementation uses service account authentication and does not require a stored BigQuery password or service account key.

Secret Manager provides a foundation for future integrations that may require external credentials or sensitive configuration.

---

# 15. Automated Testing

The project includes automated unit tests using Python's built-in `unittest` framework.

The tests validate the transformation logic independently of the BigQuery loading process.

## 15.1 Test File

```text
tests/test_transform.py
```

## 15.2 Test Coverage

The implementation includes eight unit test scenarios.

| No. | Test Scenario | Expected Result |
|---|---|---|
| 1 | Valid sales record | Record is accepted |
| 2 | Missing order ID | Record is rejected |
| 3 | Zero quantity | Record is rejected |
| 4 | Negative quantity | Record is rejected |
| 5 | Invalid date | Record is rejected |
| 6 | Negative unit price | Record is rejected |
| 7 | Empty product | Record is rejected |
| 8 | Decimal quantity | Record is rejected |

## 15.3 Running Tests Locally

The tests can be executed with:

```bash
python -m unittest discover -s tests -v
```

The same test command is incorporated into the Cloud Build workflow.

## 15.4 Why Unit Testing Matters

Unit testing helps identify defects in transformation logic before the application is deployed.

It also makes future code changes safer by providing a repeatable way to check existing functionality.

The implementation demonstrates the use of automated testing as part of a cloud application delivery process rather than treating testing as a separate manual activity.

---

# 16. Deployment Process

The application was built and deployed using Google Cloud services.

The deployment process involved several stages.

## 16.1 Infrastructure Preparation

The required Google Cloud services and resources were created:

- Artifact Registry repository.
- Cloud Build GitHub connection.
- Cloud Build trigger.
- Build service account.
- Runtime service account.
- BigQuery dataset.
- BigQuery destination table.
- Cloud Run Job.

## 16.2 Source Code Preparation

The Python application was organised into separate source, test and data directories.

The required dependency was defined in:

```text
requirements.txt
```

The BigQuery Python client library was included:

```text
google-cloud-bigquery>=3.25,<4.0
```

## 16.3 GitHub Integration

The source code was pushed to the GitHub repository.

The repository was connected to Cloud Build using the second-generation GitHub connection.

## 16.4 Automated Build

The Cloud Build trigger was configured to monitor the main branch.

The build process executed the automated test stage and built the application image.

## 16.5 Image Publication

The application image was published to Artifact Registry.

## 16.6 Cloud Run Execution

The Cloud Run Job was configured to execute the built image using the runtime service account.

The job was subsequently executed successfully.

## 16.7 End-to-End Result

The successful execution demonstrated that the application could:

- Start in the Cloud Run environment.
- Read the packaged sales CSV.
- Validate and transform the source records.
- Authenticate with BigQuery.
- Load data into a staging table.
- Execute the MERGE operation.
- Clean up the staging table.
- Complete the ETL process.

---

# 17. Technical Challenges and Resolutions

A significant part of this project involved investigating and resolving practical implementation issues.

Rather than relying solely on successful deployment steps, the development process included debugging Python code, examining CSV input behaviour, resolving BigQuery schema incompatibilities and troubleshooting cloud permissions.

The following challenges were encountered during implementation.

## 17.1 Challenge 1: CSV Header Validation Failure

### Error

```text
ValueError: CSV headers do not match the expected schema.
```

### Problem

The application rejected the CSV file because the detected headers did not match the expected schema.

The headers appeared correct when viewed in the file.

However, CSV files can contain invisible characters, encoding differences and whitespace that are not immediately obvious when inspecting them manually.

### Investigation

The CSV reading process was reviewed.

The application was updated to print the headers detected by Python:

```python
print(f"Detected CSV headers: {reader.fieldnames!r}")
```

This made it possible to inspect the actual header values rather than relying on how they appeared in the editor.

### Resolution

The file was opened using:

```python
encoding="utf-8-sig"
```

The header values were also normalised:

```python
reader.fieldnames = [
    field.strip().lstrip("\ufeff")
    for field in reader.fieldnames
]
```

This improved compatibility with CSV files containing a UTF-8 byte-order mark or surrounding whitespace.

### Skills Demonstrated

- Python debugging.
- CSV file processing.
- Character encoding.
- Input validation.
- Error diagnosis.
- Defensive programming.

### Engineering Lesson

Source data should not be assumed to be perfectly formatted simply because it appears correct in a spreadsheet or text editor.

Data ingestion logic should account for encoding and formatting differences.

---

## 17.2 Challenge 2: BigQuery STRING-to-NUMERIC Schema Conversion

### Error

```text
ALTER TABLE ALTER COLUMN SET DATA TYPE requires
that the existing column type (STRING) is assignable
to the new type (NUMERIC).
```

### Problem

The Python application expected `unit_price` to be stored as a BigQuery `NUMERIC` field.

However, the existing destination table contained the field as `STRING`.

This created a mismatch between the application's expected schema and the existing BigQuery table definition.

### Investigation

The destination table schema was examined.

The application schema was also reviewed to confirm the intended data type.

The mismatch was identified:

| Field | Existing BigQuery Type | Expected Type |
|---|---|---|
| `unit_price` | STRING | NUMERIC |

An attempt to directly alter the existing column type was rejected by BigQuery because the existing STRING type was not directly assignable to NUMERIC through the attempted operation.

### Resolution

The destination schema was corrected through a table schema migration rather than relying on the unsupported direct column alteration.

The corrected destination schema used:

```text
unit_price NUMERIC
```

The Python application continued to define the field as:

```python
bigquery.SchemaField("unit_price", "NUMERIC", mode="REQUIRED")
```

Following the schema correction, the Cloud Run Job executed successfully.

### Skills Demonstrated

- BigQuery schema management.
- SQL troubleshooting.
- Data type compatibility.
- Data warehouse design.
- Python and BigQuery integration.
- Investigation of failed data loading operations.

### Engineering Lesson

The application schema and warehouse schema must be aligned.

A successful Python transformation does not guarantee that a BigQuery load or MERGE operation will succeed if the destination table uses incompatible data types.

Schema compatibility should be checked before deploying changes to an existing warehouse table.

---

## 17.3 Challenge 3: Cloud Run Job Visibility and IAM Permissions

### Problem

The Cloud Run Job had been created, but the user account initially could not list the deployed jobs.

This made it difficult to inspect the deployment through the Google Cloud Console.

### Investigation

The issue was investigated as an access-control problem rather than an application runtime failure.

The distinction between creating or executing a resource and viewing that resource through the console was important.

### Resolution

Cloud Run Viewer access was provided to the user account one with the user account registered email.

The deployed job subsequently became visible in the Cloud Run Jobs interface.

### Skills Demonstrated

- Google Cloud IAM.
- Role-based access control.
- Cloud resource permissions.
- Permission troubleshooting.
- Understanding the difference between runtime identity and user-console access.

### Engineering Lesson

Successful deployment does not automatically mean every user account has permission to view or manage the deployed resource.

Access should be assigned according to the specific task and the principle of least privilege.

---

## 17.4 Challenge 4: Cloud Run Job Failure During BigQuery Processing

### Problem

The Cloud Run Job initially failed during the BigQuery processing stage.

The failure occurred while the application was waiting for the BigQuery MERGE job to complete.

### Investigation

The application logs and BigQuery processing flow were examined.

The investigation included:

- Reviewing the Python loading function.
- Checking the staging table identifier.
- Reviewing the destination table schema.
- Examining the BigQuery job execution stage.
- Comparing application field types with destination field types.

The BigQuery `unit_price` STRING-to-NUMERIC mismatch was identified during the troubleshooting process.

### Resolution

The destination schema was aligned with the application's expected data types.

The application was also reviewed to ensure that the staging table was referenced using its fully qualified project and dataset identifier.

After the schema correction, the Cloud Run Job completed successfully.

### Skills Demonstrated

- Cloud Run application troubleshooting.
- BigQuery job execution.
- Python exception handling.
- SQL MERGE debugging.
- Schema investigation.
- Cloud application diagnostics.
- Root-cause analysis.

### Engineering Lesson

Cloud application failures should be investigated across the complete execution path.

A failure reported at the point where a query result is awaited does not necessarily mean that the SQL statement itself is the underlying problem.

The application, staging table, destination schema, IAM permissions and BigQuery job should be examined together.

---

# 18. Troubleshooting and Lessons Learned

The project provided practical experience in troubleshooting issues across different layers of a cloud data engineering application.

| Issue | Area | Investigation | Resolution |
|---|---|---|---|
| CSV headers rejected | Python ingestion | Inspected actual parsed headers | Added UTF-8 BOM handling and header normalisation |
| STRING-to-NUMERIC conversion failure | BigQuery | Compared existing and expected schemas | Corrected destination schema |
| Cloud Run Job not visible | IAM | Investigated user access permissions | Granted Cloud Run Viewer access |
| Cloud Run execution failure | Application and BigQuery | Reviewed loading logic and destination schema | Corrected schema and completed successful execution |

## 18.1 Key Technical Lessons

### 1. Validate Source Data Early

Input validation should happen before loading records into the data warehouse.

This reduces the likelihood of invalid data reaching downstream processes.

### 2. Define Explicit Schemas

Relying on inconsistent automatic type detection can create problems when integrating Python applications with BigQuery.

Explicit schemas improve predictability.

### 3. Understand IAM Scope

Permissions should be granted at the narrowest appropriate scope.

For example, Artifact Registry Writer was assigned to the specific repository rather than retaining a broader project-level permission.

### 4. Separate Build and Runtime Identities

Different application stages require different permissions.

Using separate service accounts improves control over access.

### 5. Use Automated Testing

Automated unit tests provide early feedback when transformation logic changes.

### 6. Investigate the Entire Execution Path

A cloud application depends on several integrated services.

Troubleshooting should consider the application, runtime environment, authentication, destination schema and cloud service operations.

---

# 19. Skills Demonstrated

This project demonstrates practical experience across cloud engineering, data engineering, DevOps and application development.

## 19.1 Google Cloud Engineering

- Google Cloud Platform resource configuration.
- Artifact Registry repository creation.
- Cloud Build configuration.
- GitHub integration with Cloud Build.
- Cloud Run Job deployment.
- Serverless batch execution.
- Service account creation.
- IAM permission management.
- Regional resource configuration.
- Cloud application troubleshooting.

## 19.2 Data Engineering

- ETL pipeline development.
- CSV ingestion.
- Data transformation.
- Data quality validation.
- Schema definition.
- BigQuery integration.
- Staging table design.
- SQL MERGE operations.
- Batch data processing.
- Data type compatibility.
- Temporary table management.

## 19.3 Python Development

- Modular application design.
- Python package organisation.
- CSV processing.
- Exception handling.
- Decimal validation.
- Date validation.
- Environment variable configuration.
- BigQuery client library integration.
- Automated unit testing.

## 19.4 DevOps and CI/CD

- GitHub source control.
- Cloud Build triggers.
- Automated build workflows.
- Automated test execution.
- Buildpacks-based image creation.
- Artifact Registry image publication.
- Cloud Run deployment configuration.
- Build and runtime separation.

## 19.5 Cloud Security

- IAM role assignment.
- Least-privilege permissions.
- Dedicated service accounts.
- Repository-level permissions.
- Dataset-level permissions.
- Service account authentication.
- Removal of unnecessary broad access.

## 19.6 Problem-Solving and Engineering Practice

- Debugging Python applications.
- Diagnosing CSV encoding issues.
- Investigating BigQuery schema errors.
- Troubleshooting Cloud Run execution.
- Understanding IAM permission boundaries.
- Reviewing application logs.
- Identifying data compatibility problems.
- Applying corrective changes and validating successful execution.

---

# 20. Testing and Verification

The following activities were completed or identified as additional acceptance tests.

| Test or Verification | Status |
|---|---|
| Python transformation unit tests implemented | Completed |
| CSV extraction and validation logic implemented | Completed |
| Cloud Build workflow executed successfully | Completed |
| GitHub repository connected to Cloud Build | Completed |
| Application image built and published | Completed |
| Cloud Run Job created | Completed |
| Cloud Run Job executed successfully | Completed |
| BigQuery destination schema aligned with application | Completed |
| BigQuery staging and MERGE logic implemented | Completed |
| Second execution with duplicate-count verification | Further verification required |
| Formal end-to-end idempotency acceptance test | Further verification required |
| Terraform-based infrastructure deployment | Future enhancement |
| Cloud Monitoring alert configuration | Future enhancement |

## 20.1 Recommended Idempotency Acceptance Test

The following query can be used to identify duplicate order IDs:

```sql
SELECT
    order_id,
    COUNT(*) AS record_count
FROM
    `project-09a7fa74-88ba-427a-b50.sales_cicd.sales_raw`
GROUP BY
    order_id
HAVING
    COUNT(*) > 1;
```

Expected result:

```text
No duplicate order IDs
```

The Cloud Run Job should then be executed again with the same input file.

The destination record count should remain unchanged.

This verifies that the implemented MERGE process behaves as intended for repeated processing of the same batch.

---

# 21. Business and Engineering Value

Although this is a portfolio project using sample sales data, the architecture demonstrates a pattern that can be adapted to real business data processing requirements.

## 21.1 Operational Efficiency

Automated builds reduce the need for repetitive manual application build activities.

## 21.2 Data Quality

Validation rules help prevent incomplete or incorrectly formatted sales records from entering the warehouse.

## 21.3 Data Consistency

Explicit schemas and controlled transformation logic help maintain consistent data structures.

## 21.4 Maintainability

Separating the application into source, test and orchestration components makes the code easier to maintain.

## 21.5 Security

Dedicated service accounts and scoped IAM permissions reduce unnecessary access.

## 21.6 Scalability Foundation

The use of managed cloud services provides a foundation for extending the pipeline to larger datasets and additional data sources.

The current implementation is a working portfolio foundation rather than a claim of a fully production-hardened enterprise platform.

---

# 22. Future Improvements

The project has been designed so that additional engineering capabilities can be introduced without completely redesigning the application.

The following enhancements are planned.

## 22.1 Infrastructure as Code with Terraform

Introduce Terraform to provision and manage the cloud infrastructure.

Potential resources to manage include:

- BigQuery datasets and tables.
- Artifact Registry repositories.
- Service accounts.
- IAM bindings.
- Cloud Run Jobs.
- Cloud Build configuration where supported.

This would improve infrastructure reproducibility and demonstrate Infrastructure as Code skills.

## 22.2 Cloud Storage Integration

Move the source CSV file from the application package into Cloud Storage.

This would separate application code from source data.

The pipeline could then retrieve files from a designated bucket.

## 22.3 Cloud Scheduler

Introduce Cloud Scheduler to trigger the Cloud Run Job automatically.

This would enable scheduled batch processing without requiring manual execution.

## 22.4 Pipeline Audit Table

Create a BigQuery audit table to record:

- Execution ID.
- Start time.
- Completion time.
- Source file name.
- Number of source records.
- Number of processed records.
- Number of rejected records.
- Execution status.
- Error details.

This would improve operational traceability.

## 22.5 Structured Logging

Improve application logging using structured JSON output.

This would make it easier to filter and analyse execution events in Cloud Logging.

## 22.6 Rejected-Record Management

Introduce a separate mechanism for storing rejected records.

This would allow valid records to be processed while maintaining visibility of data-quality failures, subject to clearly defined batch-processing rules.

## 22.7 Data Reconciliation

Introduce reconciliation checks to compare:

- Source record count.
- Validated record count.
- Rejected record count.
- Staging table record count.
- Destination record count.

## 22.8 Integration Testing

Introduce integration tests to validate interactions between the Python application and BigQuery.

## 22.9 Monitoring and Alerting

Configure Cloud Monitoring to detect failed job executions and notify the relevant operator.

## 22.10 Environment Separation

Introduce separate development and production environments.

This would allow application changes to be tested before promotion to production.

---

# 23. Project Outcome

This project successfully delivered a Python-based sales ETL application deployed as a Google Cloud Run Job and integrated with BigQuery.

It also established an automated CI/CD workflow using GitHub and Google Cloud Build.

The implementation included:

- A modular Python ETL application.
- CSV extraction and validation.
- Data transformation and schema enforcement.
- Automated unit tests.
- BigQuery staging and MERGE processing.
- Cloud Build-based application image creation.
- Artifact Registry image storage.
- Cloud Run Job deployment and execution.
- Dedicated build and runtime service accounts.
- Least-privilege IAM configuration.

During development, practical implementation issues involving CSV encoding, BigQuery schema compatibility, IAM access and Cloud Run execution were investigated and resolved.

The final successful Cloud Run Job execution demonstrated that the integrated application could process the sample sales dataset and complete its BigQuery loading workflow.

The project provides a practical foundation for further development in Infrastructure as Code, scheduled data processing, monitoring, observability and production-grade cloud data engineering.

---

# 24. Repository

**GitHub Repository:**

[topisky-gcp-sales-cicd-project](https://github.com/topisky21/topisky-gcp-sales-cicd-project)

---

# 25. Author

**Developed by:** Temitope Arigbede

**Project Focus:**

- Cloud Engineering
- Data Engineering
- Python
- Google Cloud Platform
- BigQuery
- CI/CD
- Serverless Computing
- Cloud Security

This project was independently designed, implemented, tested and deployed as a practical demonstration of cloud engineering and data engineering capabilities.
