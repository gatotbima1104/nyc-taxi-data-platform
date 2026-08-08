{{
    config(
        materialized='incremental',
        incremental_strategy='insert_overwrite',
        partition_by={
            "field": "pickup_date",
            "data_type": "date",
            "granularity": "day"
        },
    )
}}

with taxi_quarantine as (
    select * from {{ ref('int_taxi_quarantine') }}
)
select
    *
from taxi_quarantine