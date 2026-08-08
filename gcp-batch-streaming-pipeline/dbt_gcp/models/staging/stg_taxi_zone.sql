select
    coalesce(cast(LocationID as integer), -999) as location_id,
    coalesce(cast(Borough as string), 'Unknown') as borough,
    coalesce(cast(Zone as string), 'Unknown') as zone,
    coalesce(cast(service_zone as string), 'Unknown') as service_zone
from {{ source('raw', 'raw_zone_taxi') }}