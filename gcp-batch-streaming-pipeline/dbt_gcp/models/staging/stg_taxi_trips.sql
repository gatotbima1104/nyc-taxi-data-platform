select
    coalesce(cast(VendorID as integer), -999) as vendor_id,

    cast(lpep_pickup_datetime as timestamp) as pickup_datetime,
    cast(lpep_dropoff_datetime as timestamp) as dropoff_datetime,

    coalesce(cast(store_and_fwd_flag as string), 'Unknown') as store_and_fwd_flag,
    coalesce(cast(RatecodeID as integer), -999) as rate_code_id,
    coalesce(cast(PULocationID as numeric), -999) as pu_location_id,
    coalesce(cast(DOLocationID as numeric), -999) as do_location_id,

    coalesce(cast(passenger_count as integer), 0) as passenger_count,
    coalesce(cast(trip_distance as numeric), 0) as trip_distance,
    coalesce(cast(fare_amount as numeric), 0) as fare_amount,
    coalesce(cast(extra as numeric), 0) as extra,
    coalesce(cast(mta_tax as numeric), 0) as mta_tax,
    coalesce(cast(tip_amount as numeric), 0) as tip_amount,
    coalesce(cast(tolls_amount as numeric), 0) as tolls_amount,
    coalesce(cast(ehail_fee as numeric), 0) as ehail_fee,
    coalesce(cast(improvement_surcharge as numeric), 0) as improvement_surcharge,
    coalesce(cast(total_amount as numeric), 0) as total_amount,
    
    coalesce(cast(payment_type as string), 'Unknown') as payment_type,
    coalesce(cast(trip_type as integer), 0) as trip_type,
    coalesce(cast(congestion_surcharge as numeric), 0) as congestion_surcharge,
    coalesce(cast(cbd_congestion_fee as numeric), 0) as cbd_congestion_fee,    

from {{ source('raw', 'raw_green_taxi') }}