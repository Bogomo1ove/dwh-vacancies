import logging
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import timedelta, datetime

default_args = {'owner': 'airflow',
                'retries': 6,
                'retry_delay': timedelta(minutes=10),
                'start_date': datetime(2026, 1, 20),
                }

def take_context(**context):
    from utils.raw_to_s3 import source_to_s3
    from parsers.geekjob import GeekJob
    logging.info('success_import')
    source_to_s3(GeekJob(), context['logical_date'])
    logging.info(f'Function finished with logical_date: {context["logical_date"]}')

with DAG(
    'gj_to_s3_dag',
    default_args=default_args,
    description='Extracting data from GeekJob by last 24 hours and loading to s3.',
    schedule_interval='0 0 * * *',
    catchup=True,
    tags=['GeekJob', 'gj_to_s3']
) as dag:

    start = EmptyOperator(task_id='start')

    source_to_s3_task= PythonOperator(
        task_id='raw_to_s3_task',
        python_callable=take_context,
        provide_context=True
    )

    end = EmptyOperator(task_id='end')

    start >> source_to_s3_task >> end