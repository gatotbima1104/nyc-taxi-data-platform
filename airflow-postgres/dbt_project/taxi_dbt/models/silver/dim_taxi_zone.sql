select
    location_id::bigint,
    coalesce(borough::text, 'Unknown') as borough,
    coalesce(zone::text, 'Unknown') as zone,
    coalesce(service_zone::text, 'Unknown') as service_zone
from {{ ref('stg_taxi_zone') }}