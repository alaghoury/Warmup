"""Generic SMTP/IMAP integration helpers."""
from __future__ import annotations

import logging
from typing import Any, Mapping

logger = logging.getLogger(__name__)


def connect_account(payload: Mapping[str, Any]) -> dict[str, Any]:
    email = str(payload.get("email", "unknown@example.com"))
    host = payload.get("host", "smtp.example.com")
    logger.info("Simulating SMTP/IMAP connection for %s via %s", email, host)
    return {
        "status": "connected",
        "provider": payload.get("provider", "smtp"),
        "email": email,
        "host": host,
    }


def send_email(account: Mapping[str, Any], message: Mapping[str, Any]) -> dict[str, Any]:
    logger.info(
        "[SMTP] Sending message for %s using host %s",
        account.get("email"),
        account.get("host", "smtp.example.com"),
    )
    return {"status": "sent", "provider": account.get("provider", "smtp")}


def fetch_inbox(account: Mapping[str, Any]) -> list[dict[str, Any]]:
    logger.debug("[IMAP] Fetching inbox for %s", account.get("email"))
    return [{"id": "smtp-msg-1", "subject": "Generic warmup"}]


def move_to_inbox(account: Mapping[str, Any], message_id: str) -> dict[str, Any]:
    logger.debug(
        "[IMAP] Moving message %s to inbox for %s", message_id, account.get("email")
    )
    return {"status": "moved", "provider": account.get("provider", "smtp")}


def reply_email(account: Mapping[str, Any], message: Mapping[str, Any]) -> dict[str, Any]:
    logger.info("[SMTP] Replying to message for %s", account.get("email"))
    return {"status": "replied", "provider": account.get("provider", "smtp")}


CONNECTOR = {
    "connect_account": connect_account,
    "send_email": send_email,
    "fetch_inbox": fetch_inbox,
    "move_to_inbox": move_to_inbox,
    "reply_email": reply_email,
}
