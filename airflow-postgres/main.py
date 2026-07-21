from scripts.extract import Extract
from scripts.database_connection import DatabaseConnection
from scripts.layers import ( Loader, QualityCheck )
from scripts.configs import Config

from utils.helpers import Helper
from utils.constants import (TAXI_URL, TAXI_ZONE_LOOKUP_URL, TAXI_DATA_FILENAME, TAXI_ZONE_LOOKUP_TABLE,
                             POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD
                             )

# Make Connection
conn = DatabaseConnection(host=POSTGRES_HOST, port=POSTGRES_PORT, dbname=POSTGRES_DB,
                          user=POSTGRES_USER,password=POSTGRES_PASSWORD
                          ).get_connection_psycopg2()

qc = QualityCheck(conn)

def check_schemas_tables():
    for schema in Config.REQUIRED_SCHEMAS:
        qc.schema_exists(schema)
        
    Helper.unit_test_log("Database schemas validated")

    for table in Config.REQUIRED_BRONZE_TABLES:
        qc.table_exists(table)
    
    Helper.unit_test_log("Database tables validated")
    
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
    for load in Config.LOAD_TO_BRONZE_CONFIGS:
        qc.validate_file(load["file"])
        
    Helper.unit_test_log("Quality check file passed")
    
def load_to_bronze():
    Loader(conn).load_to_bronze()
    Helper.log(message="Load successfully")

def check_bronze_size():
    for table in ["raw_taxi_trips", "raw_taxi_lookup"]:
        qc.validate_rows(schema='bronze', table_name=table)

    Helper.unit_test_log("Rows check passed")

if __name__ == "__main__":
    check_schemas_tables()
    extract()
    check_quality_file()
    load_to_bronze()
    check_bronze_size()