# IBM Airflow DAG Project

## Project Overview
This project is part of the IBM Data Engineering Professional Certificate. It demonstrates how to create and run an Airflow DAG that extracts, transforms, and consolidates toll traffic data from multiple sources.

## Requirements
- Apache Airflow (running locally, in Docker, or another environment)
- Python 3.x
- Bash-based tools (cut, paste, awk)
  
## Project Directory Structure

- dags
  - ETL_dag.py
  - finalassignment
    - data
      - vehicle-data.csv
      - tollplaza-data.tsv
      - payment-data.txt
      - vehicle-data-extracted.csv
      - vehicle-data-extracted-tsv.csv
      - vehicle-data-extracted-fixedwidth.csv
      - consolidated-data.csv
      - staging
        - transformed_data.csv
- docker-compose.yml
- README.md


- **ETL_dag.py** – Airflow DAG that orchestrates the ETL process.
- **data/** – Directory containing source data and generated output files.
- **docker-compose.yml** – Example Docker file for running Airflow locally.

## ETL Workflow
1. Extract data from CSV (vehicle-data.csv).
2. Extract data from TSV (tollplaza-data.tsv).
3. Extract data from fixed-width file (payment-data.txt).
4. Consolidate the extracted data into a single CSV file.
5. Transform the “vehicle type” field to uppercase.

Each step uses Bash commands (cut, paste, awk) within Airflow’s BashOperator.

## Getting Started
1. Clone or download this repository.
2. Place the contents of the “dags” folder into your Airflow DAGs directory.
3. Adjust file paths in ETL_dag.py if needed.
4. Make sure you have the input files (CSV, TSV, fixed-width) in the correct directory.
5. Start Airflow (either locally or using Docker).
6. Trigger the “ETL_toll_data” DAG from the Airflow UI.\

## Docker Setup
If you prefer to run Airflow in Docker, ensure your docker-compose.yml includes volume mounts for:
- `./dags` → `/opt/airflow/dags`
- `./data` → `/opt/airflow/dags/data`

Example snippet:
```yaml
services:
  airflow:
    volumes:
      - ./dags:/opt/airflow/dags
      - ./data:/opt/airflow/dags/data

Afterward:

Run docker-compose up -d.
Access Airflow at http://localhost:8080.
Log in, find “ETL_toll_data” DAG, and trigger it.
