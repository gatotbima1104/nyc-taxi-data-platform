from datetime import datetime, timezone

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import (
    PythonOperator,
    ShortCircuitOperator,
)
from setup import DBT_PROJECT_DIR, DEFAULT_ARGS
from tasks.dbt import check_model_changes, update_dbt_hash
from tasks.empty import finish, start

with DAG(
    dag_id="generate_dbt_docs",
    start_date=datetime(2026,1,1, tzinfo=timezone.utc),
    schedule=None,
    catchup=False,
    default_args=DEFAULT_ARGS
) as dag:
    
    start_task = start()
    
    check_changes = ShortCircuitOperator(
        task_id="check_dbt_model_changes",
        python_callable=check_model_changes,
    )
    
    generate_docs = BashOperator(
        task_id="generate_dbt_docs",
        cwd=DBT_PROJECT_DIR,
        bash_command="""
            dbt docs generate \
            --vars '{"trip_year":"{{ dag_run.conf["trip_year"] }}",
                    "trip_month":"{{ dag_run.conf["trip_month"] }}"}'
        """,
    )
    
    update_hash = PythonOperator(
        task_id="update_dbt_hash",
        python_callable=update_dbt_hash,
    )
    
    finish_task = finish()
    
    (
        start_task 
        >> check_changes
        >> generate_docs
        >> update_hash
        >> finish_task
    )