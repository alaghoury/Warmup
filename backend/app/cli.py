"""Utility commands for running Alembic migrations programmatically."""
from __future__ import annotations

import os
from pathlib import Path

from alembic import command
from alembic.config import Config

from app.config import settings

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _alembic_config() -> Config:
    """Return a configured Alembic ``Config`` instance."""
    config = Config(str(PROJECT_ROOT / "alembic.ini"))
    config.set_main_option("script_location", str(PROJECT_ROOT / "alembic"))
    database_url = os.getenv("DATABASE_URL", settings.DATABASE_URL)
    config.set_main_option("sqlalchemy.url", database_url)
    return config


def upgrade() -> None:
    """Apply the latest Alembic migrations."""
    command.upgrade(_alembic_config(), "head")


def revision(message: str) -> None:
    """Create a new autogenerating Alembic revision with the given message."""
    command.revision(_alembic_config(), message=message, autogenerate=True)


__all__ = ["upgrade", "revision"]
