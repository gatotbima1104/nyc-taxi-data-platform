from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.sdk import TaskGroup
from constants.constant import BQ_DATASET_MART
from tasks.bigquery import export_processed_taxi
from tasks.dbt import (
    build_dim_zone,
    build_fact_trips_partitioned,
    build_fact_trips_partitioned_clustered,
    build_marts,
)
from tasks.quality import create_quality_group


def create_marts_group():
    with TaskGroup(
        group_id="marts_layer",
        tooltip="Raw Ingestion Layer"
    ) as marts_group:
        
        trips_partitioned = build_fact_trips_partitioned()
        trips_partitioned_clustered = build_fact_trips_partitioned_clustered()
        export_taxi = export_processed_taxi()
        dim_zone = build_dim_zone()
        marts = build_marts()
        qa_mart = create_quality_group(
            group_id="qa_mart",
            dataset=BQ_DATASET_MART,
            table="fact_taxi_trips_partitioned",
            freshness_column="pickup_datetime"
        )
        
        completed = EmptyOperator(
            task_id="completed"
        )
        
        trips_partitioned >> qa_mart
        trips_partitioned_clustered >> qa_mart
        
        qa_mart >> export_taxi
        qa_mart >> marts
        
        [export_taxi, marts] >> completed
        dim_zone >> completed
        
    return marts_group