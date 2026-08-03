{{
    config(
        materialized='incremental',
        partition_by={
            "field": "pickup_date",
            "data_type": "date",
            "granularity": "day"
        }
    )
}}

select
    *
from {{ ref('int_taxi_curated') }}