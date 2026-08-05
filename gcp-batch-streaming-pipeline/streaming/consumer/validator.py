from streaming.consumer.model import TaxiTrip


class EventValidator:
    def validate(self, trip: TaxiTrip):
        issue = None
        
        if trip.pickup_datetime >= trip.dropoff_datetime:
            issue = "Pickup after dropoff"
            
        elif trip.trip_duration_minutes <= 0:
            issue = "Non-positive trip duration"
            
        elif trip.trip_distance <= 0:
            issue = "Non-positive trip distance"

        elif trip.fare_amount < 0:
            issue = "Negative fare amount"

        elif trip.total_amount < trip.fare_amount:
            issue = "Negative total amount"

        return {
            "trip": trip,
            "is_valid": issue is None,
            "issue_description": issue
        }
    
    @staticmethod
    def partition(record, num_partitions):
        return 0 if record["is_valid"] else 1