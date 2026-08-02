from datetime import datetime, timezone

from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from constants.constant import (
    BQ_DATASET_RAW,
    BUCKET_NAME,
    PROJECT_ID,
)
from setup import DEFAULT_ARGS, GCP_CONN_ID, GCS_TRIPS_SOURCES, GCS_ZONE_SOURCES

with DAG(
    dag_id="gatot_dag_batch_pipeline_cp3",
    start_date=datetime(2026,1,1, tzinfo=timezone.utc),
    schedule=None,
    catchup=False,
    default_args=DEFAULT_ARGS
) as dag:
    
    start = EmptyOperator(task_id="start")
    
    # CHECK EXISTANCES FILE WITH SENSOR
    checked_parquet_files = []
    
    for uri in GCS_TRIPS_SOURCES["raw"]["Uris"]:
        object_name = uri.replace(f"gs://{BUCKET_NAME}/", "")
        file_name = object_name.split("/")[-1].replace(".parquet", "")
        
        sensor = GCSObjectExistenceSensor(
            task_id=f"check_{file_name}",
            bucket=BUCKET_NAME,
            object=object_name,
            google_cloud_conn_id=GCP_CONN_ID,
            timeout=300,
            poke_interval=30
        )
        
        checked_parquet_files.append(sensor)
        
    check_zone_lookup_exist = GCSObjectExistenceSensor(
        task_id="check_zone_lookup_taxi",
        bucket=BUCKET_NAME,
        object=GCS_ZONE_SOURCES["raw"]["Uris"][0].replace(f"gs://{BUCKET_NAME}/", ""),
        google_cloud_conn_id=GCP_CONN_ID,
        timeout=300,
        poke_interval=30,
    )
    
    load_trips_to_bq_raw = BigQueryInsertJobOperator(
        task_id="load_raw_trips",
        configuration={
            "load": {
                "sourceUris": GCS_TRIPS_SOURCES["raw"]["Uris"],
                "destinationTable": {
                    "projectId": PROJECT_ID,
                    "datasetId": BQ_DATASET_RAW,
                    "tableId": GCS_TRIPS_SOURCES["raw"]["table_name"]
                },
                "sourceFormat": "PARQUET",
                "writeDisposition": "WRITE_TRUNCATE",
                "createDisposition": "CREATE_IF_NEEDED",
            }
        },
        gcp_conn_id=GCP_CONN_ID,
    )
    
    load_zone_to_bq_raw = BigQueryInsertJobOperator(
            task_id="load_raw_zone",
            configuration={
                "load": {
                    "sourceUris": GCS_ZONE_SOURCES["raw"]["Uris"],
                    "destinationTable": {
                        "projectId": PROJECT_ID,
                        "datasetId": BQ_DATASET_RAW,
                        "tableId": GCS_ZONE_SOURCES["raw"]["table_name"]
                    },
                    "sourceFormat": "CSV",
                    "skipLeadingRows": 1,
                    "autodetect": True,
                    "writeDisposition": "WRITE_TRUNCATE",
                    "createDisposition": "CREATE_IF_NEEDED",
                }
            },
            gcp_conn_id=GCP_CONN_ID,
        )

    # Transformation
    install_dbt_packages = BashOperator(
        task_id="install_dbt_packages",
        bash_command="dbt deps",
        cwd="/opt/airflow/project/dbt_gcp"
    )
    
    load_staging_to_bq = BashOperator(
        task_id="load_raw_to_staging",
        bash_command="dbt build -s staging",
        cwd="/opt/airflow/project/dbt_gcp"
    )
    
    transform_to_intermediate = BashOperator(
        task_id="transform_to_intermediate",
        bash_command="dbt build -s intermediate",
        cwd="/opt/airflow/project/dbt_gcp"
    )
    
    build_marts = BashOperator(
        task_id="build_marts",
        bash_command="dbt build -s marts",
        cwd="/opt/airflow/project/dbt_gcp"
    )

    finish = EmptyOperator(task_id="finish")
    
    # Dag Flow
    start \
        >> checked_parquet_files \
            >> load_trips_to_bq_raw
    
    start \
        >> check_zone_lookup_exist \
            >> load_zone_to_bq_raw
    
    [load_trips_to_bq_raw, load_zone_to_bq_raw] \
        >> install_dbt_packages
    
    install_dbt_packages \
        >> load_staging_to_bq \
            >> transform_to_intermediate \
                >> build_marts \
                    >> finish