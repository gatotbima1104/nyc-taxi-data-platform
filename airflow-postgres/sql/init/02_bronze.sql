CREATE TABLE IF NOT EXISTS bronze.raw_taxi_trips(
    VendorID INTEGER,
    tpep_pickup_datetime TIMESTAMP,
    tpep_dropoff_datetime TIMESTAMP,
    passenger_count BIGINT,
    trip_distance NUMERIC(10,2),
    RatecodeID BIGINT,
    store_and_fwd_flag TEXT,
    PULocationID INTEGER,
    DOLocationID INTEGER,
    payment_type BIGINT,
    fare_amount NUMERIC(10,2),
    extra NUMERIC(10,2),
    mta_tax NUMERIC(10,2),
    tip_amount NUMERIC(10,2),
    tolls_amount NUMERIC(10,2),
    improvement_surcharge NUMERIC(10,2),
    total_amount NUMERIC(10,2),
    congestion_surcharge NUMERIC(10,2),
    Airport_fee NUMERIC(10,2),
    cbd_congestion_fee NUMERIC(10,2)
);

CREATE TABLE IF NOT EXISTS bronze.raw_taxi_lookup(
    LocationID BIGINT,
    Borough TEXT,
    Zone TEXT,
    service_zone TEXT
);