import os
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

# Define file paths
base_path = "/opt/airflow/data"
csv_file = os.path.join(base_path, "vehicle-data.csv")
tsv_file = os.path.join(base_path, "tollplaza-data.tsv")
fixedwidth_file = os.path.join(base_path, "payment-data.txt")
extracted_csv_file = os.path.join(base_path, "vehicle-data-extracted.csv")
extracted_tsv_file = os.path.join(base_path, "vehicle-data-extracted-tsv.csv")
extracted_fixedwidth_file = os.path.join(base_path, "vehicle-data-extracted-fixedwidth.csv")
consolidated_file = os.path.join(base_path, "consolidated-data.csv")
transformed_file = os.path.join(base_path, "staging/transformed_data.csv")

# Ensure directories exist
os.makedirs(base_path, exist_ok=True)
os.makedirs(os.path.join(base_path, "staging"), exist_ok=True)

# Define DAG arguments
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(0),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define DAG
dag = DAG(
    'ETL_toll_data',
    default_args=default_args,
    description='Apache Airflow Final assignment',
    schedule_interval=timedelta(days=1),
)

# Task 1: Extract data from CSV
extract_data_from_csv = BashOperator(
    task_id='extract_data_from_csv',
    bash_command=f"cut -d ',' -f 1,2,3,4 {csv_file} > {extracted_csv_file}",
    dag=dag,
)

# Task 2: Extract data from TSV
extract_data_from_tsv = BashOperator(
    task_id='extract_data_from_tsv',
    bash_command=f"cut -d $'\t' -f 5,6,7 {tsv_file} > {extracted_tsv_file}",
    dag=dag,
)

# Task 3: Extract data from fixed-width file
extract_data_from_fixedwidth = BashOperator(
    task_id='extract_data_from_fixedwidth',
    bash_command=f"cut -d ' ' -f 6,7 {fixedwidth_file} > {extracted_fixedwidth_file}",
    dag=dag,
)

# Task 4: Consolidate data
consolidated_data = BashOperator(
    task_id='consolidated_data',
    bash_command=f"paste -d ',' {extracted_csv_file} {extracted_tsv_file} {extracted_fixedwidth_file} > {consolidated_file}",
    dag=dag,
)

# Task 5: Transform vehicle type to uppercase
transform_data = BashOperator(
    task_id='transform_data',
    bash_command=f"awk -F, 'BEGIN {{OFS=\",\"}} {{ $4=toupper($4); print }}' {consolidated_file} > {transformed_file}",
    dag=dag,
)

# Set task dependencies
extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixedwidth >> consolidated_data >> transform_data

