"""Microsoft Outlook / Graph API integration placeholders."""
from __future__ import annotations

import logging
from typing import Any, Mapping

logger = logging.getLogger(__name__)


def _ensure_email(payload: Mapping[str, Any]) -> str:
    email = payload.get("email")
    if not email:
        raise ValueError("Email address is required for Outlook integration")
    return str(email)


def connect_account(payload: Mapping[str, Any]) -> dict[str, Any]:
    email = _ensure_email(payload)
    logger.info("Simulating Outlook OAuth connection for %s", email)
    return {
        "status": "connected",
        "provider": "outlook",
        "email": email,
        "access_token": "outlook-dev-token",
    }


def send_email(account: Mapping[str, Any], message: Mapping[str, Any]) -> dict[str, Any]:
    logger.info("[Outlook] Sending message for %s", account.get("email"))
    return {"status": "sent", "provider": "outlook"}


def fetch_inbox(account: Mapping[str, Any]) -> list[dict[str, Any]]:
    logger.debug("[Outlook] Fetching inbox for %s", account.get("email"))
    return [{"id": "outlook-msg-1", "subject": "Graph ping"}]


def move_to_inbox(account: Mapping[str, Any], message_id: str) -> dict[str, Any]:
    logger.debug(
        "[Outlook] Moving message %s to inbox for %s", message_id, account.get("email")
    )
    return {"status": "moved", "provider": "outlook"}


def reply_email(account: Mapping[str, Any], message: Mapping[str, Any]) -> dict[str, Any]:
    logger.info("[Outlook] Replying to message for %s", account.get("email"))
    return {"status": "replied", "provider": "outlook"}


CONNECTOR = {
    "connect_account": connect_account,
    "send_email": send_email,
    "fetch_inbox": fetch_inbox,
    "move_to_inbox": move_to_inbox,
    "reply_email": reply_email,
}
