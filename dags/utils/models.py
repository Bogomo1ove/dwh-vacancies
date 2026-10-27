from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Text,
    Date,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Vacancy(Base):
    __tablename__ = "vacancies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(30), nullable=False)
    vacancy_name = Column(String(500), nullable=False)
    salary = Column(String(100), nullable=True)
    location = Column(String(255), nullable=True)
    work_format = Column(String(100), nullable=True)
    category = Column(String(255), nullable=True)
    experience = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    url = Column(String(1000), nullable=False, unique=True)
    creation_date = Column(Date, nullable=True)
    loaded_at = Column(DateTime,
    server_default=func.now(),
    nullable=False,)