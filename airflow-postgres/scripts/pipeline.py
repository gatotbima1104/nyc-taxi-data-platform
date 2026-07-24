import subprocess
import shutil
from pathlib import Path

from scripts.extract import Extract
from scripts.database_connection import DatabaseConnection
from scripts.layers import ( Loader, QualityCheck )
from scripts.configs import Config

from utils.helpers import Helper
from utils.constants import (
    TAXI_URL,
    TAXI_ZONE_LOOKUP_URL,
    TAXI_DATA_FILENAME,
    TAXI_ZONE_LOOKUP_TABLE,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DB,
    POSTGRES_USER,
    POSTGRES_PASSWORD
)

def create_connection():
    conn = DatabaseConnection(
        POSTGRES_HOST,
        POSTGRES_PORT,
        POSTGRES_DB,
        POSTGRES_USER,
        POSTGRES_PASSWORD
    )
    return conn.get_connection_psycopg2()

def check_schemas_tables():
    conn = create_connection()
    qc = QualityCheck(conn)
    
    for schema in Config.REQUIRED_SCHEMAS:
        qc.schema_exists(schema)
        
    Helper.unit_test_log("Database Schemas Validated")

    for table in Config.REQUIRED_BRONZE_TABLES:
        qc.table_exists(table)
    
    Helper.unit_test_log("Database Tables Validated")
    
def extract():
    extract_files = [
        (TAXI_URL, TAXI_DATA_FILENAME),
        (TAXI_ZONE_LOOKUP_URL, TAXI_ZONE_LOOKUP_TABLE)
    ]

    extractor = Extract()
    for url, filename in extract_files:
        extractor.extract(url, filename)
    
    Helper.log(message="Extract successfully")
    
def check_quality_file():
    conn = create_connection()
    qc = QualityCheck(conn)
        
    for load in Config.LOAD_TO_BRONZE_CONFIGS:
        qc.validate_file(load["file"])
        
    Helper.unit_test_log("Quality Check File Validated")
    
def load_to_bronze():
    conn = create_connection()
    
    Loader(conn).load_to_bronze()
    Helper.log(message="Load successfully")

def check_bronze_table():
    conn = create_connection()
    qc = QualityCheck(conn)
    
    for table in Config.REQUIRED_BRONZE_TABLES:
        qc.table_exists(table)
        qc.validate_rows(table_name=table)

    Helper.unit_test_log("Bronze Tables & Rows Validated")

def build_silver_and_mart_dbt():
     Helper.log("Building Silver and Gold layers using dbt...")
     
     dbt_path = Config.DBT_DIR / "taxi_dbt"
     profile_dbt = Config.PROFILE_DBT_DIR
     month = Helper.get_trip_month(TAXI_DATA_FILENAME)
     
      # Clean old packages
     shutil.rmtree(dbt_path / "dbt_packages", ignore_errors=True)

     lock_file = dbt_path / "package-lock.yml"
     if lock_file.exists():
        lock_file.unlink()
         
     Helper.log("Installing dbt packages")
     subprocess.run(
            [
                "dbt",
                "deps"
            ],
            cwd=dbt_path,
            check=True
     )
     
     subprocess.run(
            [
                "dbt", 
                "build",
                "--profiles-dir", str(profile_dbt),
                "--vars", f'{{"trip_month":"{month}"}}'
            ],
            cwd=dbt_path,
            check=True
     )
     
     Helper.log("Silver and Gold layers built successfully.")

def check_silver_table_rows():
    conn = create_connection()
    qc = QualityCheck(conn)
    
    for table in Config.REQUIRED_SILVER_TABLES:
        qc.table_exists(table)
        qc.validate_rows(table_name=table)

    Helper.unit_test_log("Silver Tables & Rows Validated")

def check_mart_table_rows():
    conn = create_connection()
    qc = QualityCheck(conn)
    
    for table in Config.REQUIRED_MARTS_TABLES:
        qc.table_exists(table)
        qc.validate_rows(table_name=table)

    Helper.unit_test_log("Mart Tables & Rows Validated")