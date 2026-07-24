select
	pickup_date,
	count(*) as total_trips,
	round(sum(total_amount), 2) as daily_revenue,
	round(avg(total_amount), 2) as avg_daily_revenue,
	round(avg(trip_distance), 2) as avg_trip_distance,
	round(avg(trip_duration_minutes), 2) as avg_duration_minute
from {{ ref('fact_taxi_trips') }}
group by 1