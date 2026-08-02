with curated_taxi as (
    select * from {{ ref('fact_taxi_trips_partitioned') }}
)
select
    pickup_date,
    count(*) as total_trips,
    round(sum(total_amount), 2) as total_revenue,
    round(avg(total_amount), 2) as avg_revenue,
    round(sum(tip_amount), 2) as total_tip,
    round(avg(tip_amount), 2) as avg_tip,
    round(sum(fare_amount), 2) as total_fare,
    round(avg(tip_amount), 2) as avg_fare,
    round(avg(trip_distance), 2) as avg_trip_distance,
    round(avg(trip_duration_minutes), 2) as avg_trip_duration
from curated_taxi
group by 1
order by 1