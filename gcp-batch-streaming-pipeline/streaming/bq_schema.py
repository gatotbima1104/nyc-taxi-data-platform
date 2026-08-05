from copy import deepcopy


def _field(
    name: str,
    field_type: str,
    mode: str = "NULLABLE",
):
    return {
        "name": name,
        "type": field_type,
        "mode": mode,
    }


CURATED_SCHEMA = {
    "fields": [
        # Metadata
        _field("event_id", "STRING"),
        _field("event_time", "TIMESTAMP"),
        _field("publish_time", "TIMESTAMP"),
        _field("ingestion_time", "TIMESTAMP"),

        # Trip
        _field("vendor_id", "INTEGER"),
        _field("pickup_datetime", "TIMESTAMP"),
        _field("dropoff_datetime", "TIMESTAMP"),

        # Pickup
        _field("pu_location_id", "INTEGER"),
        _field("pickup_borough", "STRING"),
        _field("pickup_zone", "STRING"),
        _field("pickup_service_zone", "STRING"),

        # Dropoff
        _field("do_location_id", "INTEGER"),
        _field("dropoff_borough", "STRING"),
        _field("dropoff_zone", "STRING"),
        _field("dropoff_service_zone", "STRING"),

        # Metrics
        _field("passenger_count", "INTEGER"),
        _field("trip_distance", "FLOAT"),
        _field("trip_duration_minutes", "FLOAT"),

        # Fare
        _field("fare_amount", "FLOAT"),
        _field("extra", "FLOAT"),
        _field("mta_tax", "FLOAT"),
        _field("tip_amount", "FLOAT"),
        _field("tolls_amount", "FLOAT"),
        _field("ehail_fee", "FLOAT"),
        _field("improvement_surcharge", "FLOAT"),
        _field("congestion_surcharge", "FLOAT"),
        _field("cbd_congestion_fee", "FLOAT"),
        _field("total_amount", "FLOAT"),

        # Business
        _field("rate_code_id", "INTEGER"),
        _field("payment_type", "INTEGER"),
        _field("payment_type_name", "STRING"),
        _field("trip_type", "INTEGER"),
        _field("store_and_fwd_flag", "STRING"),
        _field("store_and_fwd_flag_name", "STRING"),

        # Derived
        _field("pickup_hour", "INTEGER"),
        _field("pickup_day_name", "STRING"),
        _field("pickup_month", "INTEGER"),
        _field("pickup_year", "INTEGER"),
        _field("is_weekend", "BOOLEAN"),
    ]
}


QUARANTINE_SCHEMA = deepcopy(CURATED_SCHEMA)

QUARANTINE_SCHEMA["fields"].append(
    _field(
        "issue_description",
        "STRING",
    )
)