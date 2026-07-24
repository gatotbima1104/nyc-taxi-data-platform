select
	pickup_hour,
	count(*) as total_trips,
	dense_rank() OVER(
		order by count(*)
	) as ranking_demand_hour
from {{ ref('fact_taxi_trips') }}
group by 1
order by ranking_demand_hour