import os

from dotenv import load_dotenv

load_dotenv()

def required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")

    return value

PROJECT_ID = required_env("PROJECT_ID")
REGION = required_env("REGION")
BUCKET_NAME = required_env("BUCKET_NAME")
TOPIC_ID = required_env("TOPIC_ID")
SUBSCRIPTION_ID = required_env("SUBSCRIPTION_ID")
BQ_DATASET_RAW = required_env("BQ_DATASET_RAW")
BQ_DATASET_STAGING = required_env("BQ_DATASET_STAGING")
BQ_DATASET_INTERMEDIATE = required_env("BQ_DATASET_INTERMEDIATE")
BQ_DATASET_MART = required_env("BQ_DATASET_MART")
BQ_DATASET_QUARANTINE = required_env("BQ_DATASET_QUARANTINE")
BQ_DATASET_STREAMING = required_env("BQ_DATASET_STREAMING")
BG_TABLE_STREAMING_CURATED = required_env("BG_TABLE_STREAMING_CURATED")
BG_TABLE_STREAMING_QUARANTINE = required_env("BG_TABLE_STREAMING_QUARANTINE")