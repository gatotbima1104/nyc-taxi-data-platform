import os

from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID") or ""
REGION = os.getenv("REGION") or "asia-southeast2"
BUCKET_NAME = os.getenv("BUCKET_NAME") or "cp3-gatot-bucket"
TOPIC_ID = os.getenv("TOPIC_ID") or "cp3-gatot-topic"
SUBSCRIPTION_ID = os.getenv("SUBSCRIPTION_ID") or "cp3-gatot-sub"
BQ_DATASET = os.getenv("BQ_DATASET") or "cp3_gatot_dataset"
BQ_TABLE = os.getenv("BQ_TABLE") or "cp3_gatot_table"

# bq datasets
BQ_DATASET_RAW = os.getenv("BQ_DATASET_RAW") or "cp3_gatot_dataset_raw"
BQ_DATASET_STAGING = os.getenv("BQ_DATASET_STAGING") or "cp3_gatot_dataset_staging"
BQ_DATASET_INTERMEDIATE = os.getenv("BQ_DATASET_INTERMEDIATE") or "cp3_gatot_dataset_intermediate"
BQ_DATASET_MART = os.getenv("BQ_DATASET_MART") or "cp3_gatot_dataset_mart"

PARQUET_PATH = Path("data/raw/green_tripdata_2026-04.parquet")
EVENTS_PER_SECOND = 1