"""Schemas for reputation monitoring."""
from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


class ReputationPoint(BaseModel):
    account_id: int
    account_email: str | None = None
    score: float = Field(..., ge=0, le=100)
    spam_score: float | None = None
    recorded_at: datetime


class ReputationStats(BaseModel):
    history: list[ReputationPoint]
    latest: ReputationPoint | None
    threshold: float
    alert: bool


__all__ = ["ReputationPoint", "ReputationStats"]
