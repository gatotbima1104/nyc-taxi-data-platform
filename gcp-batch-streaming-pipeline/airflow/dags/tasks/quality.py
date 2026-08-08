from airflow.providers.google.cloud.operators.bigquery import BigQueryCheckOperator
from airflow.sdk import TaskGroup
from constants.constant import PROJECT_ID
from setup import GCP_CONN_ID


def _create_check(
    *,
    task_id: str,
    sql: str
):
    return BigQueryCheckOperator(
        task_id=task_id,
        sql=sql,
        use_legacy_sql=False,
        gcp_conn_id=GCP_CONN_ID
    )

def check_table_exists(
    *,
    task_id: str,
    dataset: str,
    table: str
):
    return _create_check(
        task_id=task_id,
        sql=f"""
            SELECT COUNT(*)=1
            FROM `{PROJECT_ID}.{dataset}.INFORMATION_SCHEMA.TABLES`
            WHERE table_name = '{table}'
        """
    )

def check_row_count(
    *,
    task_id: str,
    dataset: str,
    table: str,
):
    return _create_check(
        task_id=task_id,
        sql=f"""
            SELECT COUNT(*) > 0
            FROM `{PROJECT_ID}.{dataset}.{table}`
        """,
    )

def check_not_null(
    *,
    task_id: str,
    dataset: str,
    table: str,
    column: str = "pickup_datetime"
):
    return _create_check(
        task_id=task_id,
        sql=f"""
            SELECT COUNT(*)=0
            FROM `{PROJECT_ID}.{dataset}.{table}`
            WHERE {column} IS NULL
        """
    )

def check_invalid_value(
    *,
    task_id: str,
    dataset: str,
    table: str,
    expression: str
):
    return _create_check(
        task_id=task_id,
        sql=f"""
            SELECT COUNT(*)=0
            FROM `{PROJECT_ID}.{dataset}.{table}`
            WHERE {expression}
        """
    )
    
def check_freshness(
    *,
    task_id: str,
    dataset: str,
    table: str,
    datetime_column: str,
):
    return _create_check(
        task_id=task_id,
        sql=f"""
        SELECT COUNT(*) > 0
        FROM `{PROJECT_ID}.{dataset}.{table}`
        WHERE
            EXTRACT(YEAR FROM {datetime_column})
                = CAST('{{{{ params.trip_year }}}}' AS INT64)
        AND
            EXTRACT(MONTH FROM {datetime_column})
                = CAST('{{{{ params.trip_month }}}}' AS INT64)
        """
    )

def create_quality_group(
    *,
    group_id: str,
    dataset: str,
    table: str,
    not_null_columns: list[str] | None = None,
    invalid_rules: dict[str, str] | None = None,
    freshness_column: str | None = None,
): 
    with TaskGroup(group_id=group_id) as tg:
        table_exists = check_table_exists(
            task_id="table_exists",
            dataset=dataset,
            table=table
        )
        
        row_count = check_row_count(
            task_id="row_count",
            dataset=dataset,
            table=table
        )
        
        prev = row_count
        table_exists >> row_count
        
        if not_null_columns:
            for col in not_null_columns:
                task = check_not_null(
                    task_id=f"{col}_not_null",
                    dataset=dataset,
                    table=table,
                    column=col,
                )
                prev >> task
                prev = task
                
        if invalid_rules:
            for task_name, rule in invalid_rules.items():
                invalid_check = check_invalid_value(
                    task_id=task_name,
                    dataset=dataset,
                    table=table,
                    expression=rule,
                )
                prev >> invalid_check
                prev = invalid_check

        if freshness_column:
            freshness = check_freshness(
                task_id="freshness",
                dataset=dataset,
                table=table,
                datetime_column=freshness_column,
            )
            prev >> freshness
        
        return tg