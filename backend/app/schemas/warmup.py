"""Schemas for warmup automation activities."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class WarmupActivityRead(BaseModel):
    id: int
    step: str
    status: str
    timestamp: datetime
    details: dict[str, Any] | None = Field(default=None)

    class Config:
        from_attributes = True


class WarmupInsight(BaseModel):
    key: str
    title: str
    description: str
