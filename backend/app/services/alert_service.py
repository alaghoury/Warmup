"""Alerting helpers for reputation monitoring."""
from __future__ import annotations

import logging
from typing import Any

from app.models import EmailAccount

logger = logging.getLogger(__name__)


def notify_reputation_drop(account: EmailAccount, current: float, previous: float) -> None:
    """Log an alert when reputation dips beyond the configured threshold."""

    logger.warning(
        "Reputation drop detected for %s: %.2f -> %.2f",
        account.email,
        previous,
        current,
    )


def send_alert(channel: str, payload: dict[str, Any]) -> None:
    """Placeholder for future integrations (email, Slack, webhooks)."""

    logger.info("Dispatching alert on %s with payload %s", channel, payload)


__all__ = ["notify_reputation_drop", "send_alert"]
