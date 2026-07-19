from scripts.extract import Extract
from scripts.database_connection import DatabaseConnection
from scripts.layers import Loader

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

# Make Connection
conn = DatabaseConnection(
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    dbname=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD
).get_connection_psycopg2()

# Extract 
def extract():
    extract_files = [
        (TAXI_URL, TAXI_DATA_FILENAME),
        (TAXI_ZONE_LOOKUP_URL, TAXI_ZONE_LOOKUP_TABLE)
    ]

    extractor = Extract()
    for url, filename in extract_files:
        extractor.extract(url, filename)
    
    Helper.log(message="Extract successfully ...")
    
def load_to_bronze():
    Loader(conn).load_to_bronze()
    Helper.log(message="Load successfully ...")

if __name__ == "__main__":
    extract()
    load_to_bronze()