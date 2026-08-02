with curated_taxi as (
    select * from {{ ref('fact_taxi_trips_partitioned') }}
)
select
    pickup_hour,
    count(*) as total_trips,
    dense_rank() over(
        order by count(*) desc
    ) as ranking
from curated_taxi
group by 1
order by ranking