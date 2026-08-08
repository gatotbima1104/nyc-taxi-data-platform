import random
import uuid
from datetime import UTC, datetime, timedelta

from streaming.producer.stats import BatchStatistics
from streaming.setup import INVALID_EVENT_RATE, INVALID_SCENARIOS


class TaxiEventGenerator:
    def __init__(self, stats: BatchStatistics):
        self.stats = stats

    @staticmethod
    def _clamp(value: float, minimum: float, maximum: float):
        return max(minimum, min(value, maximum))

    @staticmethod
    def _calculate_fare(distance: float):
        base_fare = 3.0

        fare = (
            base_fare
            + distance * 2.8
            + random.uniform(-0.5, 0.5)
        )

        return round(max(3.0, fare), 2)
    
    def _sample(self, distribution: dict):
        """ Sample categorical values using historical probability """

        return random.choices(
            distribution["values"],
            weights=distribution["weights"],
            k=1,
        )[0]

    def _sample_numeric(self, stats: dict, decimals: int = 2):
        """ Sample numeric values using Gaussian distribution """

        value = random.gauss(
            stats["mean"],
            stats["std"],
        )

        value = self._clamp(
            value,
            stats["min"],
            stats["max"],
        )

        return round(value, decimals)

    def _generate_trip_time(self):
        start = datetime(2026, 6, 1, tzinfo=UTC)
        end = datetime(2026, 7, 31, 23, 59, 59, tzinfo=UTC)

        # Random pickup time between June and July
        total_seconds = int((end - start).total_seconds())
        pickup = start + timedelta(seconds=random.randint(0, total_seconds))

        duration = max(
            1,
            int(
                self._sample_numeric(
                    self.stats.trip_duration,
                    decimals=0,
                )
            ),
        )

        dropoff = pickup + timedelta(minutes=duration)
        return pickup, dropoff

    # GENERATE INVALID EVENTS
    def __invalid_trip_distance(self, event: dict) -> dict:
        event["trip_distance"] = 0.0
        return event
    
    def __invalid_pickup_dropoff(self, event: dict) -> dict:
        pickup = datetime.fromisoformat(
            event["lpep_pickup_datetime"]
        )
        event["lpep_dropoff_datetime"] = pickup.isoformat()
        return event
    
    def __invalid_fare_amount(self, event: dict) -> dict:
        event["fare_amount"] = -5.0
        return event
    
    def __invalid_total_amount(self, event: dict) -> dict:
        event["total_amount"] = event["fare_amount"] - 1
        return event
    
    # GENERATE VALID EVENTS
    def _generate_valid_event(self):
            now = datetime.now(UTC)
            pickup_dt, dropoff_dt = self._generate_trip_time()
            distance = self._sample_numeric(self.stats.trip_distance)
            fare = self._calculate_fare(distance)
            payment = self._sample(self.stats.payment)
            vendor = self._sample(self.stats.vendor)
            passenger = self._sample(self.stats.passenger)
            pickup_zone = self._sample(self.stats.pickup_zone)
            dropoff_zone = self._sample(self.stats.dropoff_zone)
    
            while pickup_zone == dropoff_zone:
                dropoff_zone = self._sample(
                    self.stats.dropoff_zone
                )
    
            extra = random.choice([0.0, 1.0])
            mta_tax = 0.50
    
            tip = (
                round(
                    fare * random.uniform(0.10, 0.25),
                    2,
                )
                if payment == 1
                else 0.0
            )
    
            toll = random.choice([0.0, 0.0, 0.0, 2.5, 5.0])
            congestion = random.choice([0.0, 2.75])
            cbd_fee = random.choice([0.0, 0.75])
            improvement = 0.30
    
            total = round(
                fare
                + extra
                + mta_tax
                + tip
                + toll
                + improvement
                + congestion
                + cbd_fee,
                2
            )
    
            return {
                "event_id": str(uuid.uuid4()),
                "event_time": pickup_dt.isoformat(),
                "publish_time": now.isoformat(),
                "VendorID": int(vendor),
                "lpep_pickup_datetime": pickup_dt.isoformat(),
                "lpep_dropoff_datetime": dropoff_dt.isoformat(),
                "store_and_fwd_flag": random.choices(
                    ["N", "Y"],
                    weights=[98, 2],
                    k=1,
                )[0],
    
                "RatecodeID": random.choices(
                    [1, 2, 3],
                    weights=[95, 4, 1],
                    k=1,
                )[0],
    
                "PULocationID": int(pickup_zone),
                "DOLocationID": int(dropoff_zone),
                "passenger_count": int(passenger),
                "trip_distance": distance,
                "fare_amount": fare,
                "extra": extra,
                "mta_tax": mta_tax,
                "tip_amount": tip,
                "tolls_amount": toll,
                "ehail_fee": None,
                "improvement_surcharge": improvement,
                "total_amount": total,
                "payment_type": int(payment),
                "trip_type": 1,
                "congestion_surcharge": congestion,
                "cbd_congestion_fee": cbd_fee,
            }
    
    def _inject_invalid_event(self, event: dict) -> dict:
        scenario = random.choices(
            population=list(INVALID_SCENARIOS.keys()),
            weights=list(INVALID_SCENARIOS.values()),
            k=1,
        )[0]

        match scenario:
            case "trip_distance":
                return self.__invalid_trip_distance(event)

            case "pickup_dropoff":
                return self.__invalid_pickup_dropoff(event)

            case "fare_amount":
                return self.__invalid_fare_amount(event)

            case "total_amount":
                return self.__invalid_total_amount(event)

            case _:
                return event
    
    # Randomize generated based on return condition
    def _should_generate_invalid(self):
            return random.random() < INVALID_EVENT_RATE
        
    def generate(self):
        event = self._generate_valid_event()

        if self._should_generate_invalid():
            event = self._inject_invalid_event(event)

        return event