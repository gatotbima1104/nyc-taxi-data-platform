from pathlib import Path

import pandas as pd


class BatchStatistics:
    """ Learn historical distributions from batch parquet data """
    
    def __init__(self, parquet_path: str | Path):
        self.df = pd.read_parquet(parquet_path)
        self.vendor = {}
        self.payment = {}
        self.passenger = {}
        self.pickup_zone = {}
        self.dropoff_zone = {}
        self.pickup_hour = {}
        self.trip_distance = {}
        self.trip_duration = {}
        
    @staticmethod
    def _distribution(series: pd.Series) -> dict:
        """ Convert categorical values into weighted distribution """

        counts = (
            series
            .dropna()
            .value_counts(normalize=True)
            .sort_index()
        )

        return {
            "values": counts.index.tolist(),
            "weights": counts.values.tolist(),
        }

    @staticmethod
    def _numeric_stats(series: pd.Series) -> dict:
        series = series.dropna()

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        iqr = q3 - q1

        lower = max(0, q1 - 1.5 * iqr)
        upper = q3 + 1.5 * iqr

        series = series[
            (series >= lower)
            & (series <= upper)
        ]

        return {
            "mean": float(series.mean()),
            "std": float(series.std()),
            "min": float(series.min()),
            "max": float(series.max()),
            "median": float(series.median()),
        }

    def load(self):
        df = self.df.copy()

        df["trip_duration"] = (
            df["lpep_dropoff_datetime"]
            - df["lpep_pickup_datetime"]
        ).dt.total_seconds() / 60

        df["pickup_hour"] = (
            df["lpep_pickup_datetime"]
            .dt.hour
        )

        self.vendor = self._distribution(df["VendorID"])
        self.payment = self._distribution(df["payment_type"])
        self.passenger = self._distribution(df["passenger_count"])
        self.pickup_zone = self._distribution(df["PULocationID"])
        self.dropoff_zone = self._distribution(df["DOLocationID"])
        self.pickup_hour = self._distribution(df["pickup_hour"])
        self.trip_distance = self._numeric_stats(df["trip_distance"])
        self.trip_duration = self._numeric_stats(df["trip_duration"])

        return self