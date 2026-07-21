select
    locationid as location_id,
    borough,
    zone,
    service_zone
from {{ source('bronze', 'raw_taxi_lookup') }}