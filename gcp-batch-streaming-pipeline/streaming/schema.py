import uuid
from datetime import datetime, timezone


def build_event(row: dict) -> dict:
    """
    Convert a Green Taxi row into a streaming event.
    """

    return {
        # Metadata
        "event_id": str(uuid.uuid4()),
        "event_time": datetime.now(timezone.utc).isoformat(),

        # Green Taxi columns
        "VendorID": row["VendorID"],
        "lpep_pickup_datetime": row["lpep_pickup_datetime"],
        "lpep_dropoff_datetime": row["lpep_dropoff_datetime"],
        "store_and_fwd_flag": row["store_and_fwd_flag"],
        "RatecodeID": row["RatecodeID"],
        "PULocationID": row["PULocationID"],
        "DOLocationID": row["DOLocationID"],
        "passenger_count": row["passenger_count"],
        "trip_distance": row["trip_distance"],
        "fare_amount": row["fare_amount"],
        "extra": row["extra"],
        "mta_tax": row["mta_tax"],
        "tip_amount": row["tip_amount"],
        "tolls_amount": row["tolls_amount"],
        "ehail_fee": row["ehail_fee"],
        "improvement_surcharge": row["improvement_surcharge"],
        "total_amount": row["total_amount"],
        "payment_type": row["payment_type"],
        "trip_type": row["trip_type"],
        "congestion_surcharge": row["congestion_surcharge"],
        "cbd_congestion_fee": row["cbd_congestion_fee"]
    }