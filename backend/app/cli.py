"""Utility commands for running Alembic migrations programmatically."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from app.config import settings

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _alembic_env() -> dict[str, str]:
    env = os.environ.copy()
    env.setdefault("DATABASE_URL", settings.DATABASE_URL)
    return env


def upgrade() -> None:
    """Apply the latest Alembic migrations."""
    subprocess.run(["alembic", "upgrade", "head"], check=True, cwd=PROJECT_ROOT, env=_alembic_env())


def revision(message: str) -> None:
    """Create a new autogenerating Alembic revision with the given message."""
    subprocess.run(
        ["alembic", "revision", "--autogenerate", "-m", message],
        check=True,
        cwd=PROJECT_ROOT,
        env=_alembic_env(),
    )


__all__ = ["upgrade", "revision"]
