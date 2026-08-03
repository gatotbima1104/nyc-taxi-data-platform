from datetime import datetime, timezone

from airflow import DAG
from airflow.sdk import Param
from groups.intermediate import create_int_group
from groups.marts import create_marts_group
from groups.raw import create_raw_group
from groups.staging import create_stg_group
from setup import DEFAULT_ARGS
from tasks.empty import finish, start

with DAG(
    dag_id="gatot_batch_pipeline_cp3",
    start_date=datetime(2026,1,1, tzinfo=timezone.utc),
    schedule=None,
    catchup=False,
    default_args=DEFAULT_ARGS,
    params={
        "trip_year": Param("2026", type="string"),
        "trip_month": Param("04", type="string"),
    }
) as dag:
    
    start_dag = start()
    raw_layer = create_raw_group()
    stg_layer = create_stg_group()
    int_layer = create_int_group()
    marts = create_marts_group()
    finish_dag = finish()
    
    # Dag Flow
    start_dag \
        >> raw_layer \
        >> stg_layer \
        >> int_layer \
        >> marts \
        >> finish_dag