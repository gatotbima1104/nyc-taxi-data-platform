select
	payment_type,
	count(*) as total_trips,
    round(count(*) * 100.0 / sum(count(*)) over (), 2) as trip_percentage,
	round(sum(total_amount), 2) as daily_revenue,
	round(avg(total_amount), 2) as avg_daily_revenue,
	round(avg(trip_distance), 2) as avg_trip_distance,
	round(avg(trip_duration_minutes), 2) as avg_duration_minute,
	round(avg(tip_amount), 2) as avg_tip_amount
from {{ ref('fact_taxi_trips') }}
group by 1
order by 3 desc