"""Pydantic models for email integrations."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, EmailStr, Field


class IntegrationConnectRequest(BaseModel):
    email: EmailStr
    credentials: dict[str, Any] | None = None


class IntegrationConnectResponse(BaseModel):
    account_id: int
    email: EmailStr
    provider: str
    status: str
    details: dict[str, Any] | None = None


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
