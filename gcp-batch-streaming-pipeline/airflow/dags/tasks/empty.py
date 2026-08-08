from airflow.providers.standard.operators.empty import EmptyOperator


def _create_empty_task(*, task_id: str):
    return EmptyOperator(task_id=task_id)

def start():
    return _create_empty_task(task_id="start")

def finish():
    return _create_empty_task(task_id="finish")