{{
    config(
        materialized='incremental'
    )
}}

select
    *
from {{ ref('int_taxi_curated') }}