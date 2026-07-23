from datetime import timedelta

DEFAULT_ARGS = {
    'owner': 'muhamad_gatot',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
}