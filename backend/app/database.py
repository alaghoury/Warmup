"""Database session utilities."""
from __future__ import annotations

from .models import Base, SessionLocal, engine

__all__ = ["Base", "SessionLocal", "engine", "get_db"]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
