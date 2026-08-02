with curated_taxi as (
    select * from {{ ref('fact_taxi_trips_partitioned') }}
)
select 
    pickup_zone,
	count(*) as total_trips,
	round(sum(total_amount), 2) as total_revenue,
	round(avg(total_amount), 2) as avg_revenue
from curated_taxi
group by 1
order by 2 desc