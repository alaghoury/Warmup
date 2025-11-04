"""Integration API endpoints for connecting external email providers."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps import get_current_user, get_db
from app.integrations import get_connector
from app.models import EmailAccount
from app.schemas import (
    IntegrationConnectRequest,
    IntegrationConnectResponse,
    IntegrationTestRequest,
    IntegrationTestResponse,
)

router = APIRouter(prefix="/api/v1/integrations", tags=["integrations"])


@router.post("/connect/{provider}", response_model=IntegrationConnectResponse, status_code=status.HTTP_201_CREATED)
def connect_provider(
    provider: str,
    payload: IntegrationConnectRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> IntegrationConnectResponse:
    """Connect a mailbox for the authenticated user."""

    try:
        connector = get_connector(provider)
    except KeyError as exc:  # pragma: no cover - defensive guard
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    integration_payload: dict[str, Any] = {**payload.model_dump(), "provider": provider}
    try:
        connection_details = connector["connect_account"](integration_payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    warmup_mode = payload.warmup_mode or "growth"

    account = EmailAccount(
        user_id=current_user.id,
        email=payload.email,
        provider=connection_details.get("provider", provider.lower()),
        access_token=connection_details.get("access_token"),
        refresh_token=connection_details.get("refresh_token"),
        warmup_mode=warmup_mode,
    )
    db.add(account)
    db.commit()
    db.refresh(account)

    details = {
        key: value
        for key, value in connection_details.items()
        if key
        not in {"status", "provider", "email", "access_token", "refresh_token"}
    }

    return IntegrationConnectResponse(
        account_id=account.id,
        email=account.email,
        provider=account.provider,
        status=connection_details.get("status", "connected"),
        details=details or None,
        warmup_mode=account.warmup_mode,
    )


@router.post("/test", response_model=IntegrationTestResponse)
def test_provider(
    payload: IntegrationTestRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> IntegrationTestResponse:
    """Send a simulated test email and fetch a preview of the inbox."""

    account = (
        db.query(EmailAccount)
        .filter(EmailAccount.id == payload.account_id, EmailAccount.user_id == current_user.id)
        .first()
    )
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    connector = get_connector(account.provider)
    account_payload = {
        "email": account.email,
        "provider": account.provider,
        "host": payload.model_dump().get("host", "smtp.example.com"),
    }
    message = {
        "to": payload.recipient or account.email,
        "subject": payload.subject or "Warmup integration test",
        "body": payload.body or "This is a simulated warmup message.",
    }
    send_result = connector["send_email"](account_payload, message)
    inbox_preview = connector["fetch_inbox"](account_payload)
    if inbox_preview:
        connector["move_to_inbox"](account_payload, inbox_preview[0]["id"])
        connector["reply_email"](account_payload, message)

    return IntegrationTestResponse(
        account_id=account.id,
        provider=account.provider,
        status=send_result.get("status", "ok"),
        inbox_preview=inbox_preview,
    )
