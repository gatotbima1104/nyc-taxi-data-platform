{{ config(materialized='table') }}

select
    vendor_id::integer,
    pickup_datetime::timestamp,
    dropoff_datetime::timestamp,

    coalesce(passenger_count::integer, 0) as passenger_count,
    coalesce(trip_distance::numeric(10,2), 0) as trip_distance,
    coalesce(rate_code_id::integer, -999) as rate_code_id,

    case store_and_fwd_flag
        when 'Y' then 'Store and Forward'
        when 'N' then 'Normal'
        else 'Unknown'
    end as store_and_fwd_flag,

    pu_location_id,
    do_location_id,

    case payment_type
        when 1 then 'Credit Card'
        when 2 then 'Cash'
        when 3 then 'No Charge'
        when 4 then 'Dispute'
        when 0 then 'Unknown'
        ELSE 'Unknown'
    end as payment_type,

    coalesce(fare_amount::numeric(10,2), -999) as fare_amount,
    coalesce(tip_amount::numeric(10,2), -999) as tip_amount,
    coalesce(total_amount::numeric(10,2), -999) as total_amount,

    date(pickup_datetime) as pickup_date,
    extract(hour from pickup_datetime)::integer as pickup_hour,
    trim(to_char(pickup_datetime,'Day')) as pickup_day_time,
    case 
        when extract(dow from pickup_datetime) in (0,6) then true
        else false
    end as is_weekend,
    case
        when extract(hour from pickup_datetime) between 0 and 4 then 'Late Night'
        when extract(hour from pickup_datetime) between 5 and 11 then 'Morning'
        when extract(hour from pickup_datetime) between 12 and 16 then 'Afternoon'
        when extract(hour from pickup_datetime) between 17 and 20 then 'Evening'
        else 'Night'
    end as time_period,
    round(
        (
            extract(epoch from (
                dropoff_datetime - pickup_datetime
            )) / 60   
        )::numeric,2
    ) as trip_duration_minutes,

    pickup.borough as pickup_borough,
    pickup.zone as pickup_zone,
    dropoff.borough as dropoff_borough,
    dropoff.zone as dropoff_zone,
    
    case
        when pickup_datetime >= dropoff_datetime then 'duration invalid'
        when trip_distance <= 0 then 'distance invalid'
        when passenger_count <= 0 then 'passenger invalid'
        when fare_amount <= 0 then 'fare_amount invalid'
        when tip_amount <= 0 then 'tip_amount invalid'
    end as error_type
    

from {{ ref('stg_taxi_trips') }}
left join {{ ref('stg_taxi_zone') }} pickup
    on pu_location_id = pickup.location_id
left join {{ ref('stg_taxi_zone') }} dropoff
    on do_location_id = dropoff.location_id
where pickup_datetime >= dropoff_datetime
    or trip_distance <= 0
    or passenger_count <= 0
    or fare_amount <= 0
    or tip_amount < 0