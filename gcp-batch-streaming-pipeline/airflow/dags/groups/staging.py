from airflow.sdk import TaskGroup
from constants.constant import BQ_DATASET_STAGING
from tasks.dbt import build_stg_trips, build_stg_zone, install_packages
from tasks.quality import create_quality_group


def create_stg_group():
    with TaskGroup(
        group_id="staging_layer",
        tooltip="Staging Layer"
    ) as stg_group:
        
        install_pkg = install_packages()
        taxi_trips = build_stg_trips()
        taxi_zone = build_stg_zone()
        qa_stg = create_quality_group(
            group_id="qa_stg",
            dataset=BQ_DATASET_STAGING,
            table="stg_taxi_trips",
            not_null_columns=[
                'pickup_datetime',
                'dropoff_datetime'
            ]
        )
        
        install_pkg >> taxi_trips
        install_pkg >> taxi_zone
        taxi_trips >> qa_stg
        
    return stg_group