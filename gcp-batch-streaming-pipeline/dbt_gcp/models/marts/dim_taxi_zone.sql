with taxi_zone as (
    select * from {{ ref('stg_taxi_zone') }}
)
select
    location_id,
    borough,
    zone,
    service_zone
from taxi_zone