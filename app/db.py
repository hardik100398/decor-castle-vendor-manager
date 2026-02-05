from __future__ import annotations

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


load_dotenv()


class Base(DeclarativeBase):
    """Base class for SQLAlchemy ORM models."""


def _build_database_url() -> str:
    """Build a PostgreSQL URL purely from individual DB_* env vars."""
    db_user = os.getenv("DB_USER", "newuser")
    db_password = os.getenv("DB_PASSWORD", "SuperStrongPass123!")
    db_host = os.getenv("DB_HOST", "127.0.0.1")
    db_port = os.getenv("DB_PORT", "5433")
    db_name = os.getenv("DB_NAME", "vendor_manager")

    return (
        f"postgresql+psycopg://{db_user}:{db_password}"
        f"@{db_host}:{db_port}/{db_name}"
    )


DATABASE_URL = _build_database_url()

engine = create_engine(DATABASE_URL, echo=False, future=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    """FastAPI dependency that yields a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

