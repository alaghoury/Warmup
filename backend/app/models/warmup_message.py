"""Model for stored warmup messages and spam diagnostics."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class WarmupMessage(Base):
    """Persisted record of a warmup email and spam-check insights."""

    __tablename__ = "warmup_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    account_id: Mapped[int | None] = mapped_column(
        ForeignKey("email_accounts.id", ondelete="SET NULL"), nullable=True
    )
    activity_id: Mapped[int | None] = mapped_column(
        ForeignKey("warmup_activities.id", ondelete="SET NULL"), nullable=True
    )
    domain: Mapped[str | None] = mapped_column(String(255), nullable=True)
    subject: Mapped[str | None] = mapped_column(String(255), nullable=True)
    spam_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    spam_details: Mapped[dict | None] = mapped_column(JSON, nullable=True, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )


__all__ = ["WarmupMessage"]
