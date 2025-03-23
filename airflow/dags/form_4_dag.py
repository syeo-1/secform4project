from airflow.decorators import task, dag
from datetime import timedelta, datetime

default_args = {
    'owner': 'syeo-1',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

@dag(
    dag_id = 'form_4_dag',
    default_args = default_args,
    start_date = datetime(2024, 3, 23),
    schedule_interval = '@once'
)
def hello_world_etl():

    @task
    def get_name():
        return 'sean'
    
    @task
    def get_age():
        return 19
    
    @task
    def greet(name, age):
        print(f'hello, my name is {name} and my age is {age}')

    
    name = get_name()
    age = get_age()
    greet(name=name, age=age)

greet_dag = hello_world_etl()


