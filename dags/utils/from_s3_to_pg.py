import json

from datetime import datetime

from sqlalchemy import select

from utils.database import SessionLocal
from utils.minio_conn import Object
from utils.models import Vacancy


def normalize_value(value):
    if isinstance(value, list):
        return ", ".join(value)

    return value


def parse_creation_date(value: str):
    return datetime.strptime(
        value,
        "%d.%m.%Y",
    ).date()


def load_from_s3_to_pg(
    bucket_name: str,
    object_name: str,
):
    session = SessionLocal()

    response = Object.get(
        bucket_name,
        object_name,
    )

    try:
        vacancies = json.loads(
            response.read().decode("utf-8")
        )

        for vacancy in vacancies:

            existing_vacancy = session.execute(
                select(Vacancy).where(
                    Vacancy.url == vacancy["url"]
                )
            ).scalar_one_or_none()

            if existing_vacancy:
                continue

            creation_date = parse_creation_date(
                vacancy["creation_date"]
                ),

            work_format = normalize_value(
                vacancy.get("work_format")
            )

            category = normalize_value(
                vacancy.get("category")
            )

            db_vacancy = Vacancy(
                source=vacancy["source"],
                vacancy_name=vacancy["title"],
                salary=vacancy.get("salary"),
                location=vacancy.get("location"),
                work_format=work_format,
                category=category,
                description=vacancy.get(
                    "description"
                ),
                experience=vacancy.get(
                    "experience"
                ),
                url=vacancy["url"],
                creation_date=creation_date,
            )

            session.add(db_vacancy)

        session.commit()

    finally:
        response.close()
        response.release_conn()
        session.close()