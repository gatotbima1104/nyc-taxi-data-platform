select
    *,

    date(pickup_datetime) as pickup_date,
    format_date('%A', date(pickup_datetime)) AS pickup_day_name,

    extract(hour from pickup_datetime) as pickup_hour,
    extract(month from pickup_datetime) as pickup_month,
    extract(year from pickup_datetime) as pickup_year,

    timestamp_diff(
        dropoff_datetime,
        pickup_datetime,
        minute
    ) as trip_duration_minutes,

from {{ ref('stg_taxi_trips') }}