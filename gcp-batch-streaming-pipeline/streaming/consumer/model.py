from dataclasses import dataclass
from datetime import datetime


@dataclass
class TaxiTrip:
    event_id: str
    event_time: str
    publish_time: str
    ingestion_time: datetime

    vendor_id: int
    pickup_datetime: datetime
    dropoff_datetime: datetime
    
    pu_location_id: int
    pickup_borough: str
    pickup_zone: str
    pickup_service_zone: str

    do_location_id: int
    dropoff_borough: str
    dropoff_zone: str
    dropoff_service_zone: str

    passenger_count: int
    trip_distance: float
    trip_duration_minutes: float
    
    fare_amount: float
    extra: float
    mta_tax: float
    tip_amount: float
    tolls_amount: float
    ehail_fee: float | None
    improvement_surcharge: float
    congestion_surcharge: float
    cbd_congestion_fee: float
    total_amount: float

    rate_code_id: int

    payment_type: int
    payment_type_name: str

    trip_type: int

    store_and_fwd_flag: str
    store_and_fwd_flag_name: str

    pickup_hour: int
    pickup_day_name: str
    pickup_month: int
    pickup_year: int
    is_weekend: bool