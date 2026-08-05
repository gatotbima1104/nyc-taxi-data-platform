import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PARQUET_FILE = RAW_DATA_DIR / "green_tripdata_2026-04.parquet"
TAXI_ZONE_LOOKUP = RAW_DATA_DIR / "taxi_zone_lookup.csv"
EVENTS_PER_INTERVAL = 1
PUBLISH_INTERVAL_SECONDS = 1

PROJECT_ID = os.getenv("PROJECT_ID") or "jcdeah-009"
REGION = os.getenv("REGION") or "asia-southeast2"
TOPIC_ID = os.getenv("TOPIC_ID") or "cp3-gatot-topic"
TEMP_BUCKET_NAME = os.getenv("TEMP_BUCKET_NAME") or "cp3-gatot-streaming-temp"
SUBSCRIPTION_ID = os.getenv("SUBSCRIPTION_ID") or "cp3-gatot-sub"
SUBSCRIPTION_PATH = f"projects/{PROJECT_ID}/subscriptions/{SUBSCRIPTION_ID}"

REQUIRED_FIELDS = [
    "event_id",
    "event_time",
    "ingestion_time",
    "VendorID",
    "lpep_pickup_datetime",
    "lpep_dropoff_datetime",
    "trip_distance",
    "fare_amount",
    "total_amount",
]

PAYMENT_TYPE = {
    1: "Credit Card",
    2: "Cash",
    3: "No Charge",
    4: "Dispute"
}

STORE_AND_FWD_FLAG = {
    "Y": "Store and Forward",
    "N": "Normal"
}