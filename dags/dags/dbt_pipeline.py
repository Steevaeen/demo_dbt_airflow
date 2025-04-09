from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
   'dbt_pipeline',
    start_date=datetime(2025, 4, 5),
    schedule_interval='@daily',
    catchup=False,
    max_active_runs=1
) as dag:
    
    run_dbt = BashOperator(
        task_id='run_dbt',
        bash_command='docker exec demo_dbt_airflow-dbt-1 dbt run --profiles-dir /usr/app/dbt',
        env={
            'DBT_PROFILES_DIR': '/usr/app/dbt'
        }
    )