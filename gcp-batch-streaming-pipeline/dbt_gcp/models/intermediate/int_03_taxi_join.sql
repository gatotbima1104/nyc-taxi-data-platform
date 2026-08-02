select
    t.*,

    pu.zone as pickup_zone,
    pu.borough as pickup_borough,
    pu.service_zone as pickup_service_zone,

    do.zone as dropoff_zone,
    do.borough as dropoff_borough,
    do.service_zone as dropoff_service_zone

from {{ ref('int_02_taxi_business') }} t

left join {{ ref('stg_taxi_zone') }} pu
    on t.pu_location_id = pu.location_id
left join {{ ref('stg_taxi_zone') }} do
    on t.do_location_id = do.location_id