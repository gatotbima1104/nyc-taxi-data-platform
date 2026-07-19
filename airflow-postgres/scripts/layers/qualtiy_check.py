import os
import csv
import pyarrow.parquet as pq
from datetime import datetime
from scripts.configs import Config
from utils.helpers import Helper
from pathlib import Path

class QualityCheck:
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def __init__(self, conn):
        self.conn = conn
        
    def __file_exists(self, filepath: str, timestamp=timestamp) -> None:
        """ Check file exists """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"[FAIL] File not found {filepath}")
        
        Helper.unit_test_log("Check Existing File ✓")
        
    def __file_not_empty(self, filepath: str) -> None:
        """ Check file not empty """
        if os.path.getsize(filepath) == 0:
            raise ValueError(f"[FAIL] File is empty {filepath}")
        
        Helper.unit_test_log("Check File not empty ✓")
        
    def __validate_parquet(self, filepath: str) -> pq.ParquetFile:
        """ Validate parquet """
        try:
            Helper.unit_test_log("Validating File ✓")
            return pq.ParquetFile(filepath)
        except Exception as e:
            raise ValueError(f"[FAIL] Invalid parquet file: {e}")
        
    def __validate_required_columns(self, actual_columns: list[str], req_columns: list[str]) -> None:
        """" Check required columns """
        missing_cols = []
        
        for col in req_columns:
            if col not in actual_columns:
                missing_cols.append(col)
                
        if missing_cols:
            raise ValueError(
                f"[FAIL] Missing required columns: {', '.join(missing_cols)}"
            )
        
        Helper.unit_test_log("Validate required columns ✓")

    def validate_file(self, filepath: Path):
        """" Validate parquet """
        self.__file_exists(filepath)
        self.__file_not_empty(filepath)
        
        if filepath.suffix == ".parquet":
            pq = self.__validate_parquet(filepath)
            self.__validate_required_columns(
                pq.schema_arrow.names,
                Config.REQUIRE_PARQUET_COLUMNS
            )
        elif filepath.suffix == ".csv":
            with filepath.open(newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                columns = next(reader)
                
            self.__validate_required_columns(
                columns,
                Config.REQUIRE_CSV_COLUMNS
            )
        else:
            raise ValueError(f"[FAIL] Unsupported type file: {filepath}")