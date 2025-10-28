"""Database models and engine configuration for the Warmup app."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Use a SQLite database stored alongside the backend package by default.
DATABASE_PATH = Path(__file__).resolve().parent / "app.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# SQLite requires the ``check_same_thread`` flag when sharing the connection
# across multiple threads (as FastAPI does).
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    future=True,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class User(Base):
    """Simple user model backed by SQLite."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, nullable=False)
    status = Column(String, default="active", nullable=False)


class WarmingTask(Base):
    __tablename__ = "warming_tasks"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, nullable=False, index=True)
    kind = Column(String, default="email", nullable=False)
    state = Column(String, default="queued", nullable=False)


def init_db() -> None:
    """Create database tables if they do not exist."""

    Base.metadata.create_all(bind=engine)


__all__ = [
    "Base",
    "engine",
    "SessionLocal",
    "User",
    "Account",
    "WarmingTask",
    "init_db",
]
