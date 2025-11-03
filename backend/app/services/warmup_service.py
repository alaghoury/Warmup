"""Warmup automation service helpers."""
from __future__ import annotations

import asyncio
import logging
from typing import Any, Awaitable, Callable

from sqlalchemy.orm import Session

from app.models import WarmupActivity

logger = logging.getLogger(__name__)


async def _record_activity(
    db: Session, step: str, status: str, details: dict[str, Any] | None = None
) -> WarmupActivity:
    """Persist a warmup activity row and return it."""

    activity = WarmupActivity(step=step, status=status, details=details or {})
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
        details={"recipients": recipients},
    )


async def mark_as_non_spam(db: Session) -> WarmupActivity:
    """Simulate marking a message as non-spam."""

    logger.info("Marking warmup message as not spam")
    await asyncio.sleep(0)
    return await _record_activity(
        db,
        step="mark_as_non_spam",
        status="completed",
        details={"action": "moved to inbox"},
    )


async def open_email(db: Session) -> WarmupActivity:
    """Simulate opening a warmup email."""

    logger.info("Opening warmup message to improve engagement metrics")
    await asyncio.sleep(0)
    return await _record_activity(
        db,
        step="open_email",
        status="completed",
        details={"engagement": "opened"},
    )


async def mark_as_important(db: Session) -> WarmupActivity:
    """Simulate marking an email as important."""

    logger.info("Tagging warmup message as important")
    await asyncio.sleep(0)
    return await _record_activity(
        db,
        step="mark_as_important",
        status="completed",
        details={"label": "important"},
    )


async def reply_to_email(db: Session, reply_rate: float = 0.75) -> WarmupActivity:
    """Simulate replying to a warmup email."""

    logger.info("Replying to warmup message with configured rate %s", reply_rate)
    await asyncio.sleep(0)
    return await _record_activity(
        db,
        step="reply_to_email",
        status="completed",
        details={"reply_rate": reply_rate},
    )


WARMUP_SEQUENCE: tuple[Callable[[Session], Awaitable[WarmupActivity]], ...] = (
    send_test_email,
    mark_as_non_spam,
    open_email,
    mark_as_important,
    reply_to_email,
)
