from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor
from constants.constant import BUCKET_NAME
from setup import GCP_CONN_ID, GCS_TRIPS_SOURCES, GCS_ZONE_SOURCES


def _create_gcs_sensor(
    *,
    task_id: str,
    bucket: str,
    object: str,
    **kwargs
):
    """ [DAG] Create sensor """
    return GCSObjectExistenceSensor(
            task_id=task_id,
            bucket=bucket,
            object=object,
            google_cloud_conn_id=GCP_CONN_ID,
            timeout=300,
            poke_interval=30,
            **kwargs
        )

def sensor_taxi_trips():
    """ [DAG] Sensor taxi trips """
    sensors = []
    
    for uri in GCS_TRIPS_SOURCES["raw"]["Uris"]:
        obj_name = uri.replace(f"gs://{BUCKET_NAME}/", "")
        file_name = obj_name.split("/")[-1].replace(".parquet", "")
        
        sensors.append(        
            _create_gcs_sensor(
                task_id=f"check_{file_name}",
                bucket=BUCKET_NAME,
                object=obj_name,
            )
        )
        
    return sensors
        
def sensor_taxi_zone():
    """ [DAG] Sensor taxi zone """
    obj_name = GCS_ZONE_SOURCES["raw"]["Uris"][0].replace(f"gs://{BUCKET_NAME}/", "")
    
    return _create_gcs_sensor(
        task_id="check_taxi_zone",
        bucket=BUCKET_NAME,
        object=obj_name
    )