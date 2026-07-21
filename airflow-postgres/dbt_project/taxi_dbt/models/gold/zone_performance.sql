select
	pickup_zone,
	count(*) AS total_trips,
	round(sum(total_amount), 2) as total_revenue,
	round(avg(total_amount), 2) as avg_revenue
from {{ ref('fact_taxi_trips') }}
group by 1
order by 2 desc