from airflow.providers.standard.operators.bash import BashOperator
from setup import DBT_PROJECT_DIR, MART_TABLES_ANALYSIS


def _dbt_build(
    *,
    task_id: str,
    target: str,  
    **kwargs
):
    """ [DAG] Build dbt model """
    return BashOperator(
        task_id=task_id,
        bash_command=(
            f'dbt build -s {target} '
            '--vars \'{{ {"trip_year": params.trip_year, "trip_month": params.trip_month} | tojson }}\''
        ),
        cwd=DBT_PROJECT_DIR,
        **kwargs
    )
  
def install_packages():
    """ [DAG] Install dbt pakcages """
    return BashOperator(
        task_id="install_dbt_packages",
        bash_command="dbt deps",
        cwd=DBT_PROJECT_DIR
    )
     
def build_stg_trips():
    """ [DAG] Build stg_trips """
    return _dbt_build(
        task_id="stg_taxi_trips",
        target="stg_taxi_trips"
    )

def build_stg_zone():
    """ [DAG] Build stg_zone """
    return _dbt_build(
        task_id="stg_taxi_zone",
        target="stg_taxi_zone"
    )

def build_int_enriched():
    """ [DAG] Build int_enriched """
    return _dbt_build(
        task_id="int_taxi_enriched",
        target="int_01_taxi_enriched"
    )

def build_int_business():
    """ [DAG] Build int_business """
    return _dbt_build(
        task_id="int_taxi_business",
        target="int_02_taxi_business"
    )
    
def build_int_join():
    """ [DAG] Build int_join """
    return _dbt_build(
        task_id="int_taxi_join",
        target="int_03_taxi_join"
    )

def build_int_curated():
    """ [DAG] Build int_curated """
    return _dbt_build(
        task_id="int_taxi_curated",
        target="int_taxi_curated"
    )
    
def build_int_quarantine():
    """ [DAG] Build int_quarantine """
    return _dbt_build(
        task_id="int_taxi_quarantine",
        target="int_taxi_quarantine"
    )
    
def build_fact_trips_partitioned():
    """ [DAG] Build fact_trips_partitioned """
    return _dbt_build(
        task_id="fact_taxi_trips_partitioned",
        target="fact_taxi_trips_partitioned"
    )
    
def build_fact_trips_non_partition():
    """ [DAG] Build fact_trips_non_partitioned """
    return _dbt_build(
        task_id="fact_taxi_trips_non_partition",
        target="fact_taxi_trips_non_partition"
    )

def build_fact_trips_partitioned_clustered():
    """ [DAG] Build fact_trips_partitioned_clustered """
    return _dbt_build(
        task_id="fact_taxi_trips_partitioned_clustered",
        target="fact_taxi_trips_partitioned_clustered"
    )
    
def build_dim_zone():
    """ [DAG] Build dim_zone """
    return _dbt_build(
        task_id="dim_taxi_zone",
        target="dim_taxi_zone"
    )
    
def buid_marts():
    """ [DAG] Build marts """
    tasks = []
    
    for mart in MART_TABLES_ANALYSIS:
        tasks.append (
            _dbt_build(
                task_id=f"build_{mart}",
                target=mart
            )
        )
    return tasks