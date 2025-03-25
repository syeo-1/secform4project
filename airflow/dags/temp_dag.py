from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

dag = DAG(
    "list_directories",
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
)

list_dirs = BashOperator(
    task_id="list_dirs",
    bash_command="ls -R /opt/airflow",  # Change path based on your setup
    dag=dag,
)
