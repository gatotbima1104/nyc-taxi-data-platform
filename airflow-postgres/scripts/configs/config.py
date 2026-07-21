from pathlib import Path

class Config:
    
    PANDAS_NULLABLE_INTS = [
            "VendorID",
            "passenger_count",
            "RatecodeID",
            "PULocationID",
            "DOLocationID",
            "payment_type"
            ]
    
    REQUIRE_PARQUET_COLUMNS = [
            "VendorID",
            "tpep_pickup_datetime",
            "tpep_dropoff_datetime",
            "passenger_count",
            "trip_distance",
            "RatecodeID",
            "PULocationID",
            "DOLocationID",
            "payment_type",
            "fare_amount",
            "tip_amount",
            "tolls_amount",
            "total_amount"
            ]
    
    REQUIRE_CSV_COLUMNS = [ 
            "LocationID",
            "Borough",
            "Zone",
            "service_zone"
            ]

    LOAD_TO_BRONZE_CONFIGS = [
        {
            "file": Path("data/raw/yellow_tripdata_2026_01.parquet"),
            "table": "raw_taxi_trips",
            "layer": "bronze",
            "type": "parquet",
            "required_columns": REQUIRE_PARQUET_COLUMNS,
        },
        {
            "file": Path("data/raw/taxi_zone_lookup.csv"),
            "table": "raw_taxi_lookup",
            "layer": "bronze",
            "type": "csv",
            "required_columns": REQUIRE_CSV_COLUMNS,
        },
    ]
    BRONZE = {
            "RAW_TAXI_TRIPS": "bronze.raw_taxi_trips",
            "RAW_TAXI_LOOKUP": "bronze.raw_taxi_lookup"
    }
    
    REQUIRED_SCHEMAS = [
            "bronze",
            "audit"
            ]
    
    REQUIRED_TABLES = [
            "bronze.raw_taxi_trips",
            "bronze.raw_taxi_lookup",
            "silver.taxi_trips",
            "silver.dim_taxi_zones",
            "silver.data_quality_issues",
            "gold.daily_summary",
            "gold.hourly_demand",
            "gold.zone_performance",
            "gold.payment_behavior",
            "gold.route_performance",
            "audit.logs"
            ]
    
    REQUIRED_BRONZE_TABLES = [
            "bronze.raw_taxi_trips", 
            "bronze.raw_taxi_lookup"
            ]
    
    REQUIRED_SILVER_TABLES = [
            "silver.fact_taxi_trips",
            "silver.dim_taxi_zone",
            "silver.data_quality_issues",
            ]
    
    REQUIRED_MARTS_TABLES = [
            "gold.daily_summary",
            "gold.hourly_demand",
            "gold.payment_behavior",
            "gold.route_performance",
            "gold.zone_performance"
            ]
    