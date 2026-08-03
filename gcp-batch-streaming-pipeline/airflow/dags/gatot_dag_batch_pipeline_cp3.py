from datetime import datetime, timezone

from airflow import DAG
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.sdk import Param
from setup import DEFAULT_ARGS
from tasks.bigquery import raw_taxi_trips, raw_taxi_zone
from tasks.dbt import (
    buid_marts,
    build_dim_zone,
    build_fact_trips_non_partition,
    build_fact_trips_partitioned,
    build_fact_trips_partitioned_clustered,
    build_int_business,
    build_int_curated,
    build_int_enriched,
    build_int_join,
    build_int_quarantine,
    build_stg_trips,
    build_stg_zone,
    install_packages,
)
from tasks.sensor import sensor_taxi_trips, sensor_taxi_zone

with DAG(
    dag_id="gatot_dag_batch_pipeline_cp3",
    start_date=datetime(2026,1,1, tzinfo=timezone.utc),
    schedule=None,
    catchup=False,
    default_args=DEFAULT_ARGS,
    params={
        "trip_year": Param("2026", type="string"),
        "trip_month": Param("04", type="string"),
    }
) as dag:
    
    start = EmptyOperator(task_id="start")
    
    trip_sensors = sensor_taxi_trips()
    zone_sensors = sensor_taxi_zone()
    load_raw_taxi_trips = raw_taxi_trips()
    load_raw_taxi_zone = raw_taxi_zone()

    # Transformation
    install_packages = install_packages()
    stg_taxi_trips = build_stg_trips()
    stg_taxi_zone = build_stg_zone()
    int_taxi_enriched = build_int_enriched()
    int_taxi_business = build_int_business()
    int_taxi_join = build_int_join()
    int_taxi_curated = build_int_curated()
    int_taxi_quarantine = build_int_quarantine()
    fact_trips_non_partition = build_fact_trips_non_partition()
    fact_trips_partitioned = build_fact_trips_partitioned()
    fact_trips_partitioned_clustered = build_fact_trips_partitioned_clustered()
    dim_zone = build_dim_zone()
    marts = buid_marts()
    
    finish = EmptyOperator(task_id="finish")
    
    # Dag Flow
    start >> trip_sensors >> load_raw_taxi_trips    
    start >> zone_sensors >> load_raw_taxi_zone
    
    [load_raw_taxi_trips, load_raw_taxi_zone] >> install_packages
    install_packages >> [stg_taxi_trips, stg_taxi_zone] >> int_taxi_enriched >> int_taxi_business >> int_taxi_join 
                                         
    int_taxi_join >> [int_taxi_curated, int_taxi_quarantine]
    
    int_taxi_curated >> [
        fact_trips_non_partition,
        fact_trips_partitioned,
        fact_trips_partitioned_clustered,
    ]
    
    stg_taxi_zone >> dim_zone
    
    fact_trips_partitioned >> marts
    
    marts >> finish