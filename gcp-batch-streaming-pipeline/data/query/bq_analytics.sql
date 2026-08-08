-- PRODUCTION

-- daily summary batch
select * FROM `jcdeah-009.cp3_gatot_dataset_mart.mart_daily_summary`
-- payment analysis batch
select * FROM `jcdeah-009.cp3_gatot_dataset_mart.mart_payment_analysis`
-- mosly zone batch
select * FROM `jcdeah-009.cp3_gatot_dataset_mart.mart_zone_performance`
-- peak hour batch
select * FROM `jcdeah-009.cp3_gatot_dataset_mart.mart_time_analysis`

-- Most Profitable Pickup Zones (Historical)
SELECT 
    *
FROM `jcdeah-009.cp3_gatot_dataset_mart.mart_route_analysis`
ORDER BY total_revenue DESC
LIMIT 10;

-- Top Peak Hours (Historical vs. Streaming)
WITH batch AS (
    SELECT
        EXTRACT(HOUR FROM pickup_datetime) AS hour_of_day,
        COUNT(*) AS historical_trips
    FROM `jcdeah-009.cp3_gatot_dataset_mart.fact_taxi_trips_partitioned`
    GROUP BY hour_of_day
),
streaming AS (
    SELECT
        EXTRACT(HOUR FROM pickup_datetime) AS hour_of_day,
        COUNT(*) AS streaming_trips
    FROM `jcdeah-009.cp3_gatot_dataset_streaming.trips_curated`
    GROUP BY hour_of_day
)
SELECT
    COALESCE(b.hour_of_day, s.hour_of_day) AS hour_of_day,
    historical_trips,
    streaming_trips
FROM batch b
FULL OUTER JOIN streaming s
USING (hour_of_day)
ORDER BY historical_trips DESC, streaming_trips DESC;

-- Top Pickup Zones (Historical vs. Streaming)
WITH batch AS (
    SELECT
        pickup_zone,
        COUNT(*) AS historical_trips,
        SUM(total_amount) AS historical_revenue
    FROM `jcdeah-009.cp3_gatot_dataset_mart.fact_taxi_trips_partitioned`
    GROUP BY pickup_zone
),
streaming AS (
    SELECT
        pickup_zone,
        COUNT(*) AS streaming_trips,
        SUM(total_amount) AS streaming_revenue
    FROM `jcdeah-009.cp3_gatot_dataset_streaming.trips_curated`
    GROUP BY pickup_zone
)
SELECT
    COALESCE(b.pickup_zone, s.pickup_zone) AS pickup_zone,
    IFNULL(historical_trips, 0) AS historical_trips,
    IFNULL(streaming_trips, 0) AS streaming_trips,
    ROUND(IFNULL(historical_revenue, 0), 2) AS historical_revenue,
    ROUND(IFNULL(streaming_revenue, 0), 2) AS streaming_revenue
FROM batch b
FULL OUTER JOIN streaming s
USING (pickup_zone)
ORDER BY historical_trips DESC, streaming_trips DESC;

-- Payment Method Distribution (Historical vs Streaming)
WITH batch AS (
    SELECT
        payment_type_name,
        COUNT(*) AS historical_trips
    FROM `jcdeah-009.cp3_gatot_dataset_mart.fact_taxi_trips_partitioned`
    GROUP BY payment_type_name
),
streaming AS (
    SELECT
        payment_type_name,
        COUNT(*) AS streaming_trips
    FROM `jcdeah-009.cp3_gatot_dataset_streaming.trips_curated`
    GROUP BY payment_type_name
)

SELECT
    COALESCE(b.payment_type_name,s.payment_type_name) AS payment_type,
    historical_trips,
    streaming_trips
FROM batch b
FULL OUTER JOIN streaming s
USING(payment_type_name)
ORDER BY historical_trips DESC, streaming_trips DESC;