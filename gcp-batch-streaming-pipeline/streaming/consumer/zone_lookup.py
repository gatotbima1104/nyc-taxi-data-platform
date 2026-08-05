import pandas as pd
from pandas import DataFrame
from streaming.config import TAXI_ZONE_LOOKUP


class TaxiZoneLookup:
    def __init__(self):
        df: DataFrame = pd.read_csv(TAXI_ZONE_LOOKUP)
        
        self.lookup = (
            df.set_index("LocationID").to_dict("index")
        )
        
    def get(self, location_id: int):
        return self.lookup.get(
            location_id,
            {
                "Borough": "Unknown",
                "Zone": "Unknown",
                "service_zone": "Unknown",
            }
        )