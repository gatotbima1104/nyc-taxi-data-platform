from datetime import UTC, datetime

from streaming.consumer.model import TaxiTrip
from streaming.setup import PAYMENT_TYPE, STORE_AND_FWD_FLAG


class TaxiTransformer:
    def __init__(self, zone_lookup):
        self.zone_lookup = zone_lookup
    
    def _enrich_time(self, event: dict):
        pickup = datetime.fromisoformat(event.pop("lpep_pickup_datetime"))
        dropoff = datetime.fromisoformat(event.pop("lpep_dropoff_datetime"))
        
        event["pickup_datetime"] = pickup
        event["dropoff_datetime"] = dropoff
        
        event["trip_duration_minutes"] = (
            dropoff - pickup
        ).total_seconds() / 60
        event["pickup_hour"] = pickup.hour
        event["pickup_day_name"] = pickup.strftime("%A")
        event["pickup_month"] = pickup.month
        event["pickup_year"] = pickup.year
        event["is_weekend"] = pickup.weekday() >= 5

    def _join_zone(self, event: dict):
        event["pu_location_id"] = int(event.pop("PULocationID"))
        pickup_zone = self.zone_lookup.get(
            event["pu_location_id"]
        )
        event["pickup_borough"] = pickup_zone["Borough"]
        event["pickup_zone"] = pickup_zone["Zone"]
        event["pickup_service_zone"] = pickup_zone["service_zone"]
        
        event["do_location_id"] = int(event.pop("DOLocationID"))
        dropoff_zone = self.zone_lookup.get(
            event["do_location_id"]
        )
        event["dropoff_borough"] = dropoff_zone["Borough"]
        event["dropoff_zone"] = dropoff_zone["Zone"]
        event["dropoff_service_zone"] = dropoff_zone["service_zone"]
        
    def _business_mapping(self, event: dict):
        event["payment_type"] = int(event["payment_type"])
        event["payment_type_name"] = PAYMENT_TYPE.get(
            event["payment_type"],
            "Unknown"
        )
        event["store_and_fwd_flag"] = str(event["store_and_fwd_flag"])
        event["store_and_fwd_flag_name"] = STORE_AND_FWD_FLAG.get(
            event["store_and_fwd_flag"],
            "Unknown",
        )
    
    def _standardize(self, event: dict):
        event["vendor_id"] = int(event.pop("VendorID"))
        event["ingestion_time"] = datetime.now(UTC)
        event["rate_code_id"] = int(event.pop("RatecodeID"))
        event["passenger_count"] = int(event["passenger_count"])
        event["trip_distance"] = float(event["trip_distance"])
        event["fare_amount"] = float(event["fare_amount"])
        event["extra"] = float(event["extra"])
        event["mta_tax"] = float(event["mta_tax"])
        event["tip_amount"] = float(event["tip_amount"])
        event["tolls_amount"] = float(event["tolls_amount"])
        event["total_amount"] = float(event["total_amount"])        
        event["improvement_surcharge"] = float(event["improvement_surcharge"])
        event["congestion_surcharge"] = float(event["congestion_surcharge"])
        event["cbd_congestion_fee"] = float(event["cbd_congestion_fee"])
        event["trip_type"] = int(event["trip_type"])
        event["ehail_fee"] = (
            float(event["ehail_fee"])
            if event["ehail_fee"] is not None
            else None
        )
    
    def transform(self, event: dict) -> TaxiTrip:
        self._standardize(event)
        self._enrich_time(event)
        self._join_zone(event)
        self._business_mapping(event)

        return TaxiTrip(
            event_id=event["event_id"],
            event_time=event["event_time"],
            publish_time=event["publish_time"],
            ingestion_time=event["ingestion_time"],

            vendor_id=event["vendor_id"],
            pickup_datetime=event["pickup_datetime"],
            dropoff_datetime=event["dropoff_datetime"],

            pu_location_id=event["pu_location_id"],
            pickup_borough=event["pickup_borough"],
            pickup_zone=event["pickup_zone"],
            pickup_service_zone=event["pickup_service_zone"],

            do_location_id=event["do_location_id"],
            dropoff_borough=event["dropoff_borough"],
            dropoff_zone=event["dropoff_zone"],
            dropoff_service_zone=event["dropoff_service_zone"],

            passenger_count=event["passenger_count"],
            trip_distance=event["trip_distance"],
            trip_duration_minutes=event["trip_duration_minutes"],

            fare_amount=event["fare_amount"],
            extra=event["extra"],
            mta_tax=event["mta_tax"],
            tip_amount=event["tip_amount"],
            tolls_amount=event["tolls_amount"],
            ehail_fee=event["ehail_fee"],
            improvement_surcharge=event["improvement_surcharge"],
            congestion_surcharge=event["congestion_surcharge"],
            cbd_congestion_fee=event["cbd_congestion_fee"],
            total_amount=event["total_amount"],

            rate_code_id=event["rate_code_id"],
            payment_type=event["payment_type"],
            payment_type_name=event["payment_type_name"],

            trip_type=event["trip_type"],

            store_and_fwd_flag=event["store_and_fwd_flag"],
            store_and_fwd_flag_name=event["store_and_fwd_flag_name"],

            pickup_hour=event["pickup_hour"],
            pickup_day_name=event["pickup_day_name"],
            pickup_month=event["pickup_month"],
            pickup_year=event["pickup_year"],
            is_weekend=event["is_weekend"],
        )