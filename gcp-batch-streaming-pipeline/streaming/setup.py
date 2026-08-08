from pathlib import Path

from constants.constant import PROJECT_ID, SUBSCRIPTION_ID

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PARQUET_FILE = RAW_DATA_DIR / "green_tripdata_2026-04.parquet"
TAXI_ZONE_LOOKUP = RAW_DATA_DIR / "taxi_zone_lookup.csv"
EVENTS_PER_INTERVAL = 1
PUBLISH_INTERVAL_SECONDS = 1
INVALID_EVENT_RATE = 0.05

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

INVALID_SCENARIOS = {
    "trip_distance": 40,
    "pickup_dropoff": 30,
    "fare_amount": 15,
    "total_amount": 15,
}
