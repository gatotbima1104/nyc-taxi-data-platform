from pathlib import Path

class Config:
        
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    DATA_DIR = PROJECT_ROOT / "data"
    RAW_DATA_DIR = DATA_DIR / "raw"
    SQL_DIR = PROJECT_ROOT / "sql"
    DBT_DIR = PROJECT_ROOT / "dbt_project"
    PROFILE_DBT_DIR = DBT_DIR / ".dbt"
    
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
            "file": RAW_DATA_DIR / "yellow_tripdata_2026-01.parquet",
            "table": "raw_taxi_trips",
            "layer": "bronze",
            "type": "parquet",
            "required_columns": REQUIRE_PARQUET_COLUMNS,
        },
        {
            "file": RAW_DATA_DIR / "taxi_zone_lookup.csv",
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
    