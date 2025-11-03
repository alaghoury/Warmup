"""Schemas for domain and spam diagnostics."""
from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel


class SpamSummary(BaseModel):
    count: int
    average_score: float | None
    latest_score: float | None
    last_checked_at: datetime | None
    provider: str | None = None


class DomainCheckResponse(BaseModel):
    domain: str
    mx_records: list[str]
    blacklist_hits: list[str]
    warnings: list[str]
    checked_at: datetime
    spam: SpamSummary


__all__ = ["DomainCheckResponse", "SpamSummary"]
