"""Warmup automation activity tracking model."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class WarmupActivity(Base):
    """Represents a recorded step in the email warmup automation pipeline."""

    __tablename__ = "warmup_activities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    step: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    details: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True, default=dict)

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return (
            f"WarmupActivity(id={self.id!r}, step={self.step!r}, "
            f"status={self.status!r}, timestamp={self.timestamp!r})"
        )
