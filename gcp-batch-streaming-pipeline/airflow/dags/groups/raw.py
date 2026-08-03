from airflow.sdk import TaskGroup
from tasks.bigquery import raw_taxi_trips, raw_taxi_zone
from tasks.sensor import sensor_taxi_trips, sensor_taxi_zone


def create_raw_group():
    with TaskGroup(
        group_id="raw_layer",
        tooltip="Raw Ingestion Layer"
    ) as raw_group:
        
        trip_sensor = sensor_taxi_trips()
        zone_sensor = sensor_taxi_zone()
        load_trip = raw_taxi_trips()
        load_zone = raw_taxi_zone()
        
        trip_sensor >> load_trip
        zone_sensor >> load_zone
        
    return raw_group