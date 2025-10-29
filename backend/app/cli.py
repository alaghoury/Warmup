"""Utility commands for running Alembic migrations programmatically."""

from __future__ import annotations

import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def upgrade() -> None:
    """Apply the latest Alembic migrations."""
    subprocess.run(["alembic", "upgrade", "head"], check=True, cwd=PROJECT_ROOT)


def revision(message: str) -> None:
    """Create a new autogenerating Alembic revision with the given message."""
    subprocess.run(
        ["alembic", "revision", "--autogenerate", "-m", message],
        check=True,
        cwd=PROJECT_ROOT,
    )


__all__ = ["upgrade", "revision"]
