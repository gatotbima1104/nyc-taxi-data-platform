with curated_taxi as (
    select * from {{ ref('fact_taxi_trips_partitioned') }}
)
select
    pickup_zone,
    dropoff_zone,
    count(*) as total_trips,
    round(avg(total_amount), 2) as avg_revenue,
	round(sum(total_amount), 2) as total_revenue
from curated_taxi
group by 1,2
order by 3 desc