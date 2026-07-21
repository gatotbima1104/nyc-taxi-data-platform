select
	pickup_zone,
	dropoff_zone,
	count(*) AS total_trips,
	round(avg(total_amount), 2) as avg_revenue,
	round(sum(total_amount), 2) as total_revenue
from {{ ref('fact_taxi_trips') }}
group by 1,2
order by 5 desc