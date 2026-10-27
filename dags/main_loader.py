from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from parsers import GeekJob
from utils.from_s3_to_pg import load_from_s3_to_pg
from utils.raw_to_s3 import source_to_s3


default_args = {
    "owner": "airflow",
    "retries": 6,
    "retry_delay": timedelta(minutes=10),
    "start_date": datetime(2026, 10, 25),
}


def load_to_s3(source, **context):
    source_to_s3(
        source,
        context["logical_date"],
    )


def load_to_pg(bucket_name, **context):
    logical_date = context["logical_date"]

    object_name = (
        logical_date.strftime("%d.%m.%Y")
        + ".json"
    )

    load_from_s3_to_pg(
        bucket_name=bucket_name,
        object_name=object_name,
    )


with DAG(
    dag_id="main-loader-dag",
    default_args=default_args,
    description=(
        "Extract vacancies from GeekJob "
        "and load them to MinIO and PostgreSQL."
    ),
    schedule_interval="0 0 * * *",
    tags=["raw"],
) as dag:

    gj_to_s3_task = PythonOperator(
        task_id="gj_to_s3",
        python_callable=load_to_s3,
        op_kwargs={
            "source": GeekJob(),
        },
    )

    gj_to_pg_task = PythonOperator(
        task_id="gj_to_pg",
        python_callable=load_to_pg,
        op_kwargs={
            "bucket_name": "geekjobvacancies",
        },
    )

    gj_to_s3_task >> gj_to_pg_task