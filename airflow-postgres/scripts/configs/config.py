from pathlib import Path

class Config:
    PANDAS_NULLABLE_INTS = [
        "VendorID",
        "passenger_count",
        "RatecodeID",
        "PULocationID",
        "DOLocationID",
        "payment_type",
    ],
    LOAD_TO_BRONZE_CONFIGS = [
        {
            "file": Path("data/raw/yellow_tripdata_2026_01.parquet"),
            "table": "raw_taxi_trips",
            "layer": "bronze"
        },
        {
            "file": Path("data/raw/taxi_zone_lookup.csv"),
            "table": "raw_taxi_lookup",
            "layer": "bronze"
        },
    ],
    BRONZE = {
        "RAW_TAXI_TRIPS": "bronze.raw_taxi_trips",
        "RAW_TAXI_LOOKUP": "bronze.raw_taxi_lookup"
    }