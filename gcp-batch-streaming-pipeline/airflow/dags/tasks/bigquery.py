from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from constants.constant import (
    BQ_DATASET_RAW,
    PROJECT_ID,
)
from setup import GCP_CONN_ID, GCS_TRIPS_SOURCES, GCS_ZONE_SOURCES


def _create_load_task(
    *,
    task_id: str,
    source_uris: list[str],
    table_name: str,
    source_format: str,
    **load_options
):
    """ [DAG] Load GCS to BiqQuery """
    return BigQueryInsertJobOperator(
        task_id=task_id,
        configuration={
            "load": {
                "sourceUris": source_uris,
                "destinationTable": {
                    "projectId": PROJECT_ID,
                    "datasetId": BQ_DATASET_RAW,
                    "tableId": table_name
                },
                "sourceFormat": source_format,
                "writeDisposition": "WRITE_TRUNCATE",
                "createDisposition": "CREATE_IF_NEEDED",
                **load_options
            }
        },
        gcp_conn_id=GCP_CONN_ID,
    )

def raw_taxi_trips():
    """ [DAG] load raw trips """
    return _create_load_task(
        task_id="load_raw_trips",
        source_uris=GCS_TRIPS_SOURCES["raw"]["uri"],
        table_name=GCS_TRIPS_SOURCES["raw"]["table_name"],
        source_format='PARQUET'
    )

def raw_taxi_zone():
    """ [DAG] Load raw zone """
    return _create_load_task(
        task_id="load_raw_zone",
        source_uris=GCS_ZONE_SOURCES["raw"]["uri"],
        table_name=GCS_ZONE_SOURCES["raw"]["table_name"],
        source_format='CSV',
        skipLeadingRows=1,
        autodetect=True,
    )