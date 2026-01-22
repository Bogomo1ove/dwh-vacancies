import logging
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import timedelta, datetime

default_args = {'owner': 'airflow',
                'retries': 3,
                'retry_delay': timedelta(minutes=1),
                'start_date': datetime(2026, 1, 20),
                }

def take_context(**context):
    from utils.raw_to_s3 import source_to_s3
    from parsers.headhunter import HeadHunter
    logging.info('success_import')
    source_to_s3(HeadHunter(), context['logical_date'])
    logging.info(f'Function finished with logical_date: {context["logical_date"]}')

with DAG(
    'hh_to_s3_dag',
    default_args=default_args,
    description='Extracting data from HeadHunter by last 24 hours and loading to s3.',
    schedule_interval='0 0 * * *',
    catchup=True,
    tags=['hh', 'hh_to_s3']
) as dag:

    start = EmptyOperator(task_id='start')

    source_to_s3_task= PythonOperator(
        task_id='raw_to_s3_task',
        python_callable=take_context,
        provide_context=True
    )

    end = EmptyOperator(task_id='end')

    start >> source_to_s3_task >> end