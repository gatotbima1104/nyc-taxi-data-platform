from psycopg2.extensions import connection as PGConnection
from io import StringIO
from pandas import DataFrame
from enum import StrEnum
from datetime import datetime

from utils.helpers import Helper
from scripts.configs.config import Config
from scripts.managers import (
    SchemaManager,
    AuditManager
)

class Layer(StrEnum):
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"

class Loader:
    def __init__(self, conn: PGConnection):
        self.conn = conn
        self.schema = SchemaManager(conn)
        self.audit = AuditManager(conn)
        
    def _normalize_dtypes(self, df: DataFrame) -> DataFrame:
        """" Normalize tables """
        
        for column in Config.PANDAS_NULLABLE_INTS:
            if column in df.columns:
                df[column] = df[column].astype("Int64")
        return df

    def _load_to_pg(self, filepath: str, table_name: str, layer: Layer | None = None) -> None:
        """" Load to postgres """
        df = self._normalize_dtypes(Helper.load_file(filepath))
        buffer = StringIO()

        df.to_csv(buffer, index=False, header=False)
        buffer.seek(0)

        sql = f"""
        COPY bronze.{table_name}
        FROM STDIN
        WITH (FORMAT CSV)
        """
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                        TRUNCATE TABLE bronze.{table_name} RESTART IDENTITY;
                    """
                )
                cur.copy_expert(sql, buffer)

        self.conn.commit()

        Helper.log(
            f"Load to {'BRONZE' if layer == 'bronze' else 'SILVER' if layer == 'silver' else 'GOLD'} successfully loaded {len(df):,} rows --> bronze.{table_name}"
        )
    
    def load_to_bronze(self) -> None:
        """" Load to BRONZE """
        start = datetime.now()
        
        try:  
            for load in Config.LOAD_TO_BRONZE_CONFIGS:
                self._load_to_pg(
                    load["file"],
                    load["table"],
                    load["layer"]
                )
                
            rows = self.schema.count(Config.BRONZE["RAW_TAXI_TRIPS"])
            
            self.audit.log_pipeline(
                layer="BRONZE",
                process_name="LOAD_TO_BRONZE",
                start_time=start,
                end_time=datetime.now(),
                rows_processed=rows,
                status="SUCCESS",
                message="[BRONZE] Bronze layer loaded successfully."
            )
            
            Helper.log(message="Load to Bronze successfully ...")
            
        except Exception as e:
            self.conn.rollback()
            self.audit.log_pipeline(
                layer="BRONZE",
                process_name="LOAD_TO_BRONZE",
                start_time=start,
                end_time=datetime.now(),
                rows_processed=0,
                status="FAILED",
                message=f"[ERROR] {str(e)}"
            )
            raise