"""SQLAlchemy models for the Warmup application."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from .database import Base


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


__all__ = ["User", "Account", "WarmingTask"]
