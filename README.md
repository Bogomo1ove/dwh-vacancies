# DWH Vacancies

An ETL pipeline for collecting job vacancies from GeekJob and loading them into a PostgreSQL data warehouse.

The project demonstrates data extraction, raw data storage, data transformation, relational database loading, and workflow orchestration with Apache Airflow.

## Architecture

```text
                 GeekJob
                    |
                    v
             Apache Airflow
                    |
                    v
             Data Extraction
                    |
                    v
             Raw JSON Files
                    |
                    v
                 MinIO
              (Object Storage)
                    |
                    v
           Data Transformation
                    |
                    v
               PostgreSQL
             (Data Warehouse)
```

## Tech Stack

- **Python** — data extraction and transformation
- **Apache Airflow 2.10.5** — workflow orchestration
- **Docker Compose** — local development environment
- **MinIO** — S3-compatible object storage for raw JSON data
- **PostgreSQL 13** — relational storage for processed vacancies
- **SQLAlchemy** — database access and ORM
- **Requests and Beautiful Soup** — web scraping

## Data Pipeline

The main workflow is defined in `dags/main_loader.py`.

It consists of two sequential tasks:

### 1. Extract and store raw data

Task: `gj_to_s3`

- Retrieves vacancies from GeekJob.
- Collects vacancy information such as title, salary, location, work format, category, description, experience, URL, and publication date.
- Serializes the results to JSON.
- Uploads the JSON file to the `geekjobvacancies` MinIO bucket.

Files are named using the logical execution date, for example:

```text
31.07.2026.json
```

### 2. Load data into PostgreSQL

Task: `gj_to_pg`

- Reads the corresponding JSON object from MinIO.
- Converts fields into the format expected by the database.
- Parses vacancy publication dates.
- Normalizes list-valued fields, such as categories.
- Checks whether a vacancy with the same URL already exists.
- Inserts new vacancies into PostgreSQL.

The URL is used to identify existing vacancies and prevent duplicates during repeated pipeline runs.

## Database

The project stores processed vacancies in a PostgreSQL table represented by the SQLAlchemy model in `dags/utils/models.py`.

The table includes:

| Column | Description |
|---|---|
| `id` | Primary key |
| `source` | Vacancy source |
| `vacancy_name` | Vacancy title |
| `salary` | Salary information |
| `location` | Job location |
| `work_format` | Remote, hybrid, or other work format |
| `category` | Vacancy category or seniority level |
| `description` | Vacancy description |
| `experience` | Required experience |
| `url` | Vacancy URL; unique |
| `creation_date` | Vacancy publication date |
| `loaded_at` | Timestamp when the row was loaded |

## Project Structure

```text
dwh-vacancies/
├── dags/
│   ├── main_loader.py
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── geekjob.py
│   │   └── headhunter.py
│   └── utils/
│       ├── config.py
│       ├── create_tables.py
│       ├── database.py
│       ├── from_s3_to_pg.py
│       ├── get_hh_token.py
│       ├── minio_conn.py
│       ├── models.py
│       └── raw_to_s3.py
├── config/
├── plugins/
├── Dockerfile
├── docker-compose.yaml
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- Git

### 1. Clone the repository

```bash
git clone git@github.com:Bogomo1ove/dwh-vacancies.git
cd dwh-vacancies
```

### 2. Configure environment variables

Create a local `.env` file in the project root.

Configure the database connection variables required by the project:

```dotenv
DB_HOST=postgres_dwh
DB_PORT=5432
DB_USER=your_database_user
DB_PASS=your_database_password
DB_NAME=your_database_name
```

Configure MinIO credentials and any additional environment variables required by Docker Compose.

Do not commit your local `.env` file.

### 3. Start the services

```bash
docker compose up -d --build
```

Check the service status:

```bash
docker compose ps
```

### 4. Open Airflow

Open the Airflow web interface:

```text
http://localhost:8080
```

Log in using the credentials configured for your local Airflow environment.

### 5. Run the pipeline

Find the `main-loader-dag` DAG in Airflow and enable or trigger it as needed.

The workflow executes `gj_to_s3` first and then `gj_to_pg`.

## Configuration Notes

- The pipeline uses Airflow's logical execution date to determine the raw JSON object name.
- The default DAG schedule is daily at midnight according to the Airflow timezone configuration.
- The pipeline is designed to avoid inserting duplicate vacancies with an already stored URL.
- The local Docker Compose configuration is intended for development and experimentation.

## Future Improvements

- Add robust HTTP timeouts, retries, and error handling to the scraper.
- Improve logging and monitoring of extraction and loading operations.
- Add automated tests for parsing, transformations, and database loading.
- Introduce data quality checks.
- Add incremental loading metrics and pipeline observability.
- Extend the pipeline to additional job sources.
- Add dbt models for analytical transformations.

## Current Status

The GeekJob extraction and loading workflow has been tested locally with Apache Airflow, MinIO, and PostgreSQL.

The HeadHunter parser code is also present in the repository, but the main DAG currently uses GeekJob as its active source.