"""Database configuration for the Warmup application."""
from __future__ import annotations

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database file stored alongside this module
_DB_FILE = Path(__file__).resolve().parent / "warmup.db"
_DATABASE_URL = f"sqlite:///{_DB_FILE}"

# SQLite needs ``check_same_thread`` disabled for use with FastAPI's async workers.
engine = create_engine(
    _DATABASE_URL,
    connect_args={"check_same_thread": False},
    future=True,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def get_db():
    """Yield a SQLAlchemy session and ensure it is closed afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


__all__ = ["Base", "engine", "SessionLocal", "get_db"]
