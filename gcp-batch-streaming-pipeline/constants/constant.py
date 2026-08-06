import os

from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID") or "jcdeah-009"
REGION = os.getenv("REGION") or "asia-southeast2"
BUCKET_NAME = os.getenv("BUCKET_NAME") or "cp3-gatot-bucket"
TOPIC_ID = os.getenv("TOPIC_ID") or "cp3-gatot-topic"
SUBSCRIPTION_ID = os.getenv("SUBSCRIPTION_ID") or "cp3-gatot-sub"


# bq datasets
BQ_DATASET_RAW = os.getenv("BQ_DATASET_RAW") or "cp3_gatot_dataset_raw"
BQ_DATASET_STAGING = os.getenv("BQ_DATASET_STAGING") or "cp3_gatot_dataset_staging"
BQ_DATASET_INTERMEDIATE = os.getenv("BQ_DATASET_INTERMEDIATE") or "cp3_gatot_dataset_intermediate"
BQ_DATASET_MART = os.getenv("BQ_DATASET_MART") or "cp3_gatot_dataset_mart"
BQ_DATASET_QUARANTINE = os.getenv("BQ_DATASET_QUARANTINE") or "cp3_gatot_dataset_quarantine"
BQ_DATASET_STREAMING = os.getenv("BQ_DATASET_STREAMING") or "cp3_gatot_dataset_streaming"

BG_TABLE_STREAMING_CURATED = os.getenv("BG_TABLE_STREAMING_CURATED") or "trips_curated"
BG_TABLE_STREAMING_QUARANTINE = os.getenv("BG_TABLE_STREAMING_QUARANTINE") or "trips_quarantine"