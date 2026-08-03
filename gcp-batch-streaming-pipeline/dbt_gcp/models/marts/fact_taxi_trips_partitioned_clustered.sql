{{
    config(
        materialized='incremental',
        partition_by={
            "field": "pickup_date",
            "data_type": "date",
            "granularity": "day"
        },
        cluster_by=[
            'pickup_borough',
            'payment_type_name',
        ]
    )
}}

select
    *
from {{ ref('int_taxi_curated') }}