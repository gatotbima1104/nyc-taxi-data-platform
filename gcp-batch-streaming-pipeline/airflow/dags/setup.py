from datetime import timedelta
from typing import TypedDict

from constants.constant import BUCKET_NAME


class GCSSource(TypedDict):
    uris = list[str]
    table_name = str

DEFAULT_ARGS = {
    'owner': 'muhamad_gatot',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False
}

GCS_TRIPS_SOURCES: dict[str, GCSSource] = {
    "raw": {
        "Uris": [
            f"gs://{BUCKET_NAME}/raw/green_tripdata_2026-04.parquet",
            f"gs://{BUCKET_NAME}/raw/green_tripdata_2026-05.parquet"
        ],
        "table_name": "raw_green_taxi"   
    }
}

GCS_ZONE_SOURCES: dict[str, GCSSource] = {
    "raw": {
        "Uris": [
            f"gs://{BUCKET_NAME}/raw/taxi_zone_lookup.csv"
        ],
        "table_name": "raw_zone_taxi"   
    }
}

GCP_CONN_ID = "google_cloud_default"