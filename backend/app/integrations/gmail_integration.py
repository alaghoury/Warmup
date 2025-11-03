"""Gmail integration helper functions.

The implementation is intentionally lightweight: it mocks the behaviour of the
Google Workspace APIs so the rest of the application can be exercised without
real credentials.  The module exposes a dictionary of callables consumed by the
router layer.
"""
from __future__ import annotations

import logging
from typing import Any, Mapping

logger = logging.getLogger(__name__)


def _ensure_email(payload: Mapping[str, Any]) -> str:
    email = payload.get("email")
    if not email:
        raise ValueError("Email address is required for Gmail integration")
    return str(email)


def connect_account(payload: Mapping[str, Any]) -> dict[str, Any]:
    email = _ensure_email(payload)
    logger.info("Simulating Gmail OAuth connection for %s", email)
    return {
        "status": "connected",
        "provider": "gmail",
        "email": email,
        "access_token": "gmail-dev-token",
        "refresh_token": "gmail-dev-refresh",
    }


def send_email(account: Mapping[str, Any], message: Mapping[str, Any]) -> dict[str, Any]:
    logger.info("[Gmail] Sending message for %s", account.get("email"))
    return {"status": "sent", "provider": "gmail"}


def fetch_inbox(account: Mapping[str, Any]) -> list[dict[str, Any]]:
    logger.debug("[Gmail] Fetching inbox for %s", account.get("email"))
    return [{"id": "gmail-msg-1", "subject": "Warmup ping"}]


def move_to_inbox(account: Mapping[str, Any], message_id: str) -> dict[str, Any]:
    logger.debug(
        "[Gmail] Moving message %s to inbox for %s", message_id, account.get("email")
    )
    return {"status": "moved", "provider": "gmail"}


def reply_email(account: Mapping[str, Any], message: Mapping[str, Any]) -> dict[str, Any]:
    logger.info("[Gmail] Replying to message for %s", account.get("email"))
    return {"status": "replied", "provider": "gmail"}


CONNECTOR = {
    "connect_account": connect_account,
    "send_email": send_email,
    "fetch_inbox": fetch_inbox,
    "move_to_inbox": move_to_inbox,
    "reply_email": reply_email,
}
