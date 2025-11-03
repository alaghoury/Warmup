"""Pydantic models for email integrations."""
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, EmailStr, Field


WarmupMode = Literal["growth", "flat", "random"]


class IntegrationConnectRequest(BaseModel):
    email: EmailStr
    credentials: dict[str, Any] | None = None
    warmup_mode: WarmupMode | None = Field(default=None)


class IntegrationConnectResponse(BaseModel):
    account_id: int
    email: EmailStr
    provider: str
    status: str
    details: dict[str, Any] | None = None
    warmup_mode: WarmupMode


class IntegrationTestRequest(BaseModel):
    account_id: int = Field(gt=0)
    recipient: EmailStr | None = None
    subject: str | None = None
    body: str | None = None


class IntegrationTestResponse(BaseModel):
    account_id: int
    provider: str
    status: str
    inbox_preview: list[dict[str, Any]]
