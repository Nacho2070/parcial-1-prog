import os

from sqlmodel import SQLModel, Session, create_engine


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:root@localhost:5432/parcial1",
)

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables() -> None:
    # Ensure SQLModel metadata includes all tables before create_all runs.
    from . import models  # noqa: F401

    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session