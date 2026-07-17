CREATE TABLE IF NOT EXISTS gold.daily_summary (
    pickup_date TIMESTAMP NOT NULL,
    daily_revenue NUMERIC(10,2) NOT NULL,
    avg_daily_revenue NUMERIC(10,2) NOT NULL,
    avg_trip_distance NUMERIC(10,2) NOT NULL,
    avg_duration_minute NUMERIC(10,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS gold.hourly_demand_summary (
    pickup_hour INTEGER NOT NULL,
    total_trips INTEGER NOT NULL,
    ranking_demand_hour INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS gold.zone_performance_summary (
    pickup_zone TEXT NOT NULL,
    total_trips INTEGER NOT NULL,
    avg_revenue NUMERIC(10,2) NOT NULL,
    total_revenue NUMERIC(10,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS gold.payment_behavior_summary (
    payment_type TEXT NOT NULL,
    total_trips INTEGER NOT NULL,
    trip_percentage NUMERIC(10,2) NOT NULL,
    daily_revenue NUMERIC(10,2) NOT NULL,
    avg_daily_revenue NUMERIC(10,2) NOT NULL,
    avg_trip_distance NUMERIC(10,2) NOT NULL,
    avg_duration_minute NUMERIC(10,2) NOT NULL,
    avg_tip_amount NUMERIC(10,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS gold.route_performance_summary (
    pickup_zone TEXT NOT NULL,
    dropoff_zone TEXT NOT NULL,
    total_trips INTEGER NOT NULL,
    avg_revenue NUMERIC(10,2) NOT NULL,
    total_revenue NUMERIC(10,2) NOT NULL
);