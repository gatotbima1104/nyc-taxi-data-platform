from airflow.sdk import TaskGroup
from constants.constant import BQ_DATASET_INTERMEDIATE
from tasks.dbt import (
    build_int_business,
    build_int_curated,
    build_int_enriched,
    build_int_join,
    build_int_quarantine,
)
from tasks.quality import create_quality_group


def create_int_group():
    with TaskGroup(
        group_id="intermediate_layer",
        tooltip="Intermediate Transformation Layer"
    ) as int_group:
        
        enriched = build_int_enriched()
        business = build_int_business()
        join = build_int_join()
        curated = build_int_curated()
        quarantine = build_int_quarantine()
        qa_int = create_quality_group(
            group_id="qa_int",
            dataset=BQ_DATASET_INTERMEDIATE,
            table="int_taxi_curated",
            not_null_columns=[
                'pickup_datetime',
                'dropoff_datetime'
            ],
            invalid_rules={
                "invalid_trip_time": "pickup_datetime >= dropoff_datetime",
                "invalid_trip_distance": "trip_distance <= 0",
                "invalid_total_amount": "total_amount < 0",
            },
        )
        
        enriched >> business >> join
        join >> curated >> qa_int
        join >> quarantine
        
    return int_group