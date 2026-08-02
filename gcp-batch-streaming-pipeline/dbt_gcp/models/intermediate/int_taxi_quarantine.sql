select

    *,
    case
        when pickup_datetime >= dropoff_datetime then 'Pickup after dropoff'
        when trip_duration_minutes <= 0 then 'Non-positive trip duration'
        when trip_distance <= 0 then 'Non-positive trip distance'
        when total_amount <= 0 then 'Negative total amount'
        when passenger_count <= 0 then 'Invalid passenger count'
        when fare_amount <= 0 then 'Negative fare amount'
        else 'Unknown quality issue'
    end as issue_description

from {{ ref('int_03_taxi_join') }}

where pickup_datetime >= dropoff_datetime
    or trip_duration_minutes <= 0
    or trip_distance <= 0
    or total_amount <= 0
    or passenger_count <= 0
    or fare_amount <= 0