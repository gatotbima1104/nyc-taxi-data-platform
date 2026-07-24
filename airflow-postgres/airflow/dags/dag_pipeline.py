from airflow.sdk import dag, task
from datetime import datetime

from airflow.setup import DEFAULT_ARGS
from scripts.pipeline import (
    check_schemas_tables,
    extract,
    check_quality_file,
    load_to_bronze,
    check_bronze_table,
    build_silver_and_mart_dbt,
    check_silver_table_rows,   
    check_mart_table_rows,
    generate_dbt_docs
)

validate_db = task(check_schemas_tables)
extract_data = task(extract)
validate_file = task(check_quality_file)
bronze_stg = task(load_to_bronze)
validate_bronze = task(check_bronze_table)
build_silver_mart_dbt = task(build_silver_and_mart_dbt)
validate_silver = task(check_silver_table_rows)
validate_mart = task(check_mart_table_rows)
dbt_docs = task(generate_dbt_docs)

@dag(
    dag_id="taxi_pipeline",
    description="NYC Taxi Yellow Pipeline",
    default_args=DEFAULT_ARGS,
    start_date=datetime(2026, 1, 1),
    schedule="@daily", # Every days
    max_active_runs=1,
    catchup=False,
    tags=["etl", "taxi", "airflow", "dbt"]
)
def main_pipeline():
    (
        validate_db() 
        >> extract_data() 
        >> validate_file() 
        >> bronze_stg()
        >> validate_bronze()
        >> build_silver_mart_dbt() 
        >> validate_silver() 
        >> validate_mart()
        >> dbt_docs()
    )

main_pipeline()