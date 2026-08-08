from datetime import timedelta
from typing import TypedDict

from constants.constant import BUCKET_NAME


class GCSSource(TypedDict):
    uri: str
    table_name: str

DEFAULT_ARGS = {
    'owner': '',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False
}

GCS_TRIPS_SOURCES: dict[str, GCSSource] = {
    "raw": {
        "uri": f"gs://{BUCKET_NAME}/raw/green_tripdata_{{{{ params.trip_year }}}}-{{{{ params.trip_month }}}}.parquet",
        "table_name": "raw_green_taxi"   
    }
}

GCS_ZONE_SOURCES: dict[str, GCSSource] = {
    "raw": {
        "uri": f"gs://{BUCKET_NAME}/raw/taxi_zone_lookup.csv",
        "table_name": "raw_zone_taxi"   
    }
}

GCP_CONN_ID = "google_cloud_default"
DBT_PROJECT_DIR = "/opt/airflow/project/dbt_gcp"

MART_TABLES_ANALYSIS = [
    "mart_daily_summary",
    "mart_payment_analysis",
    "mart_route_analysis",
    "mart_time_analysis",
    "mart_zone_performance"
]