select
    *,

    case payment_type
        when 1 then 'Credit Card'
        when 2 then 'Cash'
        when 3 then 'No Charge'
        when 4 then 'Dispute'
        ELSE 'Unknown'
    end as payment_type_name,

    case store_and_fwd_flag
        when 'Y' then 'Store and Forward'
        when 'N' then 'Normal'
        else 'Unknown'
    end as store_and_fwd_flag_name,

    case
        when extract(hour from pickup_datetime) between 0 and 4 then 'Late Night'
        when extract(hour from pickup_datetime) between 5 and 11 then 'Morning'
        when extract(hour from pickup_datetime) between 12 and 16 then 'Afternoon'
        when extract(hour from pickup_datetime) between 17 and 20 then 'Evening'
        else 'Night'
    end as time_period,

    case 
        when extract(dayofweek from pickup_datetime) in (1,7) 
            then true
        else false
    end as is_weekend,

from {{ ref('int_01_taxi_enriched') }}