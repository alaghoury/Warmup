"""Warmup automation service helpers."""
from __future__ import annotations

import asyncio
import logging
from typing import Any, Awaitable, Callable, Iterable

from sqlalchemy.orm import Session

from app.models import WarmupActivity

logger = logging.getLogger(__name__)

WARMUP_BENEFITS: tuple[dict[str, str], ...] = (
    {
        "key": "inbox_good_standing",
        "title": "Inbox in good standing",
        "description": (
            "Regular warmup interactions keep sending habits healthy so mailbox "
            "providers view the account as trustworthy."
        ),
    },
    {
        "key": "spam_folder_avoidance",
        "title": "Spam folder avoidance",
        "description": (
            "Simulated engagement mimics real conversations to help messages land "
            "in the inbox instead of spam."
        ),
    },
    {
        "key": "reputation_monitoring",
        "title": "Reputation monitoring",
        "description": (
            "Track your Warmup Reputation Score with actionable guidance to keep "
            "performance above industry benchmarks."
        ),
    },
    {
        "key": "primary_folder_delivery",
        "title": "Landing in the primary folder",
        "description": (
            "Warmup actions are tuned to land in the primary inbox on providers "
            "like Gmail rather than Promotions."
        ),
    },
    {
        "key": "instant_alerts",
        "title": "Instant alerts",
        "description": (
            "Receive notifications if reputation dips so campaigns can pause "
            "before further damage occurs."
        ),
    },
    {
        "key": "real_inbox_network",
        "title": "Network of real inboxes",
        "description": (
            "Warmup emails circulate through a monitored network of 30,000+ "
            "authentic inboxes for realistic engagement."
        ),
    },
)

_BENEFITS_BY_KEY: dict[str, dict[str, str]] = {b["key"]: b for b in WARMUP_BENEFITS}


def get_warmup_benefits() -> list[dict[str, str]]:
    """Expose the catalog of warmup automation benefits."""

    return [dict(benefit) for benefit in WARMUP_BENEFITS]


def _resolve_benefits(keys: Iterable[str] | None) -> list[dict[str, str]]:
    if not keys:
        return []
    return [dict(_BENEFITS_BY_KEY[key]) for key in keys if key in _BENEFITS_BY_KEY]


async def _record_activity(
    db: Session,
    step: str,
    status: str,
    details: dict[str, Any] | None = None,
    benefit_keys: Iterable[str] | None = None,
) -> WarmupActivity:
    """Persist a warmup activity row and return it."""

    payload = details.copy() if details else {}
    insights = _resolve_benefits(benefit_keys)
    if insights:
        payload.setdefault("insights", insights)

    activity = WarmupActivity(step=step, status=status, details=payload)
    db.add(activity)
    db.commit()
    db.refresh(activity)
    logger.info("Warmup step %s finished with status %s", step, status)
    return activity


async def send_test_email(db: Session) -> WarmupActivity:
    """Simulate sending a warmup test email."""

    recipients = ["deliverability@warmup.dev", "qa@warmup.dev"]
    logger.info("Sending warmup test email to %s", recipients)
    await asyncio.sleep(0)
    return await _record_activity(
        db,
        step="send_test_email",
        status="completed",
        details={
            "recipients": recipients,
            "summary": "Delivered warmup test emails to trusted inbox partners.",
        },
        benefit_keys=["inbox_good_standing", "real_inbox_network"],
    )


async def mark_as_non_spam(db: Session) -> WarmupActivity:
    """Simulate marking a message as non-spam."""

    logger.info("Marking warmup message as not spam")
    await asyncio.sleep(0)
    return await _record_activity(
        db,
        step="mark_as_non_spam",
        status="completed",
        details={
            "action": "moved to inbox",
            "summary": "Reinforced inbox placement by rescuing warmup emails from spam.",
        },
        benefit_keys=["spam_folder_avoidance"],
    )


async def open_email(db: Session) -> WarmupActivity:
    """Simulate opening a warmup email."""

    logger.info("Opening warmup message to improve engagement metrics")
    await asyncio.sleep(0)
    return await _record_activity(
        db,
        step="open_email",
        status="completed",
        details={
            "engagement": "opened",
            "summary": "Registered natural engagement to strengthen reputation signals.",
        },
        benefit_keys=["primary_folder_delivery", "reputation_monitoring"],
    )


async def mark_as_important(db: Session) -> WarmupActivity:
    """Simulate marking an email as important."""

    logger.info("Tagging warmup message as important")
    await asyncio.sleep(0)
    return await _record_activity(
        db,
        step="mark_as_important",
        status="completed",
        details={
            "label": "important",
            "summary": "Boosted message priority to guide mailbox filters toward the primary tab.",
        },
        benefit_keys=["primary_folder_delivery"],
    )


async def reply_to_email(db: Session, reply_rate: float = 0.75) -> WarmupActivity:
    """Simulate replying to a warmup email."""

    logger.info("Replying to warmup message with configured rate %s", reply_rate)
    await asyncio.sleep(0)
    return await _record_activity(
        db,
        step="reply_to_email",
        status="completed",
        details={
            "reply_rate": reply_rate,
            "summary": "Simulated natural replies and triggered monitoring alerts if engagement dips.",
        },
        benefit_keys=["instant_alerts", "reputation_monitoring"],
    )


WARMUP_SEQUENCE: tuple[Callable[[Session], Awaitable[WarmupActivity]], ...] = (
    send_test_email,
    mark_as_non_spam,
    open_email,
    mark_as_important,
    reply_to_email,
)


__all__ = [
    "WARMUP_SEQUENCE",
    "get_warmup_benefits",
    "mark_as_important",
    "mark_as_non_spam",
    "open_email",
    "reply_to_email",
    "send_test_email",
]
