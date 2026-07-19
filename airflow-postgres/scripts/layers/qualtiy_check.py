import os
import pyarrow.parquet as pq

from scripts.configs import Config

class QualityCheck:
    def __init__(self, conn):
        self.conn = conn
        
    def __file_exists(self, filepath: str) -> None:
        """ Check file exists """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found {filepath}")
        
    def __file_not_empty(self, filepath: str) -> None:
        """ Check file not empty """
        if os.path.getsize(filepath) == 0:
            raise ValueError(f"File is empty {filepath}")
        
    def __validate_parquet(self, filepath: str) -> pq.ParquetFile:
        """ Validate parquet """
        try:
            return pq.ParquetFile(filepath)
        except Exception as e:
            raise ValueError(f"Invalid parquet file: {e}")
        
    def __required_columns_pq(self, pq: pq.ParquetFile, req_columns: list[str]) -> None:
        """" Check all columns required fulfilled """
        columns = pq.schema_arrow.names
        
        missing_cols = []
        
        for col in req_columns:
            if col not in columns:
                missing_cols.append(col)
                
        if missing_cols:
            raise ValueError(
                f"Missing required columns: {', '.join(missing_cols)}"
            )
            
    def validate_parquet(self, filepath: str):
        self.__file_exists(filepath)
        self.__file_not_empty(filepath)

        pq = self.__validate_parquet(filepath)
        
        self.__required_columns_pq(
            pq,
            Config.REQUIRE_PARQUET_COLUMNS
        )
        
    def validate_csv(self, filepath: str):
        self.__file_exists(filepath)
        self.__file_not_empty(filepath)