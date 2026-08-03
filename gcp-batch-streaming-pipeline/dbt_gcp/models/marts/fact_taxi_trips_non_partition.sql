{{
    config(
        materialized='incremental',
        incremental_strategy='insert_overwrite',
    )
}}

select
    *
from {{ ref('int_taxi_curated') }}