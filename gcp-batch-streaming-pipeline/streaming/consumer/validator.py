from datetime import datetime

from streaming.config import REQUIRED_FIELDS


class EventValidator:
    def validate(self, event: dict):
        errors = []

        for field in REQUIRED_FIELDS:
            if event.get(field) in (None, ""):
                errors.append(f"{field} is required")
        try:
            pickup = datetime.fromisoformat(event["lpep_pickup_datetime"])
            dropoff = datetime.fromisoformat(event["lpep_dropoff_datetime"])
            
            if pickup >= dropoff:
                errors.append("pickup must be before dropoff")

        except Exception:
            errors.append("invalid datetime")

        if event["trip_distance"] <= 0:
            errors.append("trip_distance must be > 0")

        if event["fare_amount"] < 0:
            errors.append("fare_amount must be >= 0")

        if event["total_amount"] < event["fare_amount"]:
            errors.append("total_amount invalid")

        event["validation_errors"] = errors
        event["is_valid"] = len(errors) == 0

        return event
    
    @staticmethod
    def partition(event, num_partitions):
        if event["is_valid"]:
            return 0
        return 1