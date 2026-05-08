import os

from sqlalchemy import text
from sqlmodel import SQLModel, Session, create_engine


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:root@localhost:5432/parcial1",
)

engine = create_engine(DATABASE_URL, echo=True)


def _apply_legacy_schema_fixes() -> None:
    # Existing databases may not have the new self-referencing category column yet.
    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE categoria ADD COLUMN IF NOT EXISTS parent_id INTEGER"))
        connection.execute(
            text(
                """
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1
                        FROM pg_constraint
                        WHERE conname = 'fk_categoria_parent_id_categoria'
                    ) THEN
                        ALTER TABLE categoria
                        ADD CONSTRAINT fk_categoria_parent_id_categoria
                        FOREIGN KEY (parent_id) REFERENCES categoria(id);
                    END IF;
                END $$;
                """
            )
        )


def create_db_and_tables() -> None:
    # Ensure SQLModel metadata includes all tables before create_all runs.
    from .models import models  # noqa: F401

    SQLModel.metadata.create_all(engine)
    _apply_legacy_schema_fixes()


def get_session():
    with Session(engine) as session:
        yield session