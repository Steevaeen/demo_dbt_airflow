from airflow import DAG
from airflow.operators.docker_operator import DockerOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data_team',
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    'ecommerce_metrics',
    default_args=default_args,
    start_date=datetime(2025, 4, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:

    run_dbt = DockerOperator(
        task_id='run_dbt_models',
        image='ghcr.io/dbt-labs/dbt-postgres:1.7.8',
        command='dbt run --profiles-dir /dbt',
        volumes=['./dbt_project:/dbt'],
        auto_remove=True,
        docker_url='unix://var/run/docker.sock',
        network_mode='host'
    )