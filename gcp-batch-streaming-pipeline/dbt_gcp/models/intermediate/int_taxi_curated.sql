select
    *,

from {{ ref('int_03_taxi_join') }}

where pickup_datetime < dropoff_datetime
    and trip_duration_minutes > 0
    and trip_distance > 0
    and total_amount > 0
    and passenger_count > 0
    and fare_amount > 0