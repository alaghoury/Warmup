"""Warmup automation service helpers."""
from __future__ import annotations

import asyncio
import logging
import random
from collections import defaultdict
from datetime import date
from typing import Any, Awaitable, Callable, Iterable

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import EmailAccount, WarmupActivity
from app.services.ai_reply_service import generate_human_reply
from app.services.spam_check_service import analyze_warmup_message
from app.services.reputation_service import refresh_reputation_scores

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
    account: EmailAccount | None = None,
) -> WarmupActivity:
    """Persist a warmup activity row and return it."""

    payload = details.copy() if details else {}
    if account is not None:
        payload.setdefault("account_id", account.id)
        payload.setdefault("account_email", account.email)
    insights = _resolve_benefits(benefit_keys)
    if insights:
        payload.setdefault("insights", insights)

    activity = WarmupActivity(step=step, status=status, details=payload)
    db.add(activity)
    db.commit()
    db.refresh(activity)
    logger.info("Warmup step %s finished with status %s", step, status)
    return activity


async def send_test_email(db: Session, account: EmailAccount | None = None) -> WarmupActivity:
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
        account=account,
    )


async def mark_as_non_spam(db: Session, account: EmailAccount | None = None) -> WarmupActivity:
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
        account=account,
    )


async def open_email(db: Session, account: EmailAccount | None = None) -> WarmupActivity:
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
        account=account,
    )


async def mark_as_important(db: Session, account: EmailAccount | None = None) -> WarmupActivity:
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
        account=account,
    )


async def reply_to_email(
    db: Session, account: EmailAccount | None = None, reply_rate: float = 0.75
) -> WarmupActivity:
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
        account=account,
    )


async def maybe_reply(
    db: Session,
    account: EmailAccount | None = None,
    *,
    reply_rate: float = 0.6,
    language: str = "English",
    tone: str = "friendly",
) -> WarmupActivity:
    """Optionally craft a realistic reply using the DeepSeek integration."""

    chance = random.random()
    logger.debug(
        "Evaluating AI reply for %s with chance %.2f (threshold %.2f)",
        account.email if account else "warmup",
        chance,
        reply_rate,
    )

    if chance > reply_rate:
        return await _record_activity(
            db,
            step="maybe_reply",
            status="skipped",
            details={
                "reason": "reply_rate_threshold",
                "observed_probability": chance,
                "reply_rate": reply_rate,
            },
            account=account,
        )

    email_context = (
        "Hello! We're monitoring the ongoing warmup journey for account"
        f" {account.email if account else 'the current mailbox'}."
        " Please acknowledge the latest deliverability signals."
    )
    generated = await generate_human_reply(
        email_context,
        language=language,
        tone=tone,
    )

    return await _record_activity(
        db,
        step="maybe_reply",
        status="completed",
        details={
            "language": language,
            "tone": tone,
            "reply": generated,
        },
        benefit_keys=["reputation_monitoring", "instant_alerts"],
        account=account,
    )


WARMUP_SEQUENCE: tuple[
    Callable[[Session, EmailAccount | None], Awaitable[WarmupActivity]],
    ...,
] = (
    send_test_email,
    mark_as_non_spam,
    open_email,
    mark_as_important,
    reply_to_email,
    maybe_reply,
)

_BASE_DAILY_QUOTA = 5
_MAX_GROWTH_QUOTA = 40
_RANDOM_VARIANCE = 5
_DAILY_SENDS: defaultdict[int, int] = defaultdict(int)
_DAILY_QUOTAS: dict[int, int] = {}


def compute_daily_quota(account: EmailAccount) -> int:
    """Determine the number of warmup sends permitted for an account today."""

    cached = _DAILY_QUOTAS.get(account.id)
    if cached is not None and account.warmup_mode != "random":
        return cached

    days_active = max((date.today() - account.created_at.date()).days, 0)

    if account.warmup_mode == "growth":
        quota = min(_BASE_DAILY_QUOTA + days_active, _MAX_GROWTH_QUOTA)
    elif account.warmup_mode == "flat":
        quota = _BASE_DAILY_QUOTA + 2  # steady state cadence
    elif account.warmup_mode == "random":
        quota = random.randint(_BASE_DAILY_QUOTA, _BASE_DAILY_QUOTA + _RANDOM_VARIANCE)
    else:  # pragma: no cover - defensive fallback
        quota = _BASE_DAILY_QUOTA

    _DAILY_QUOTAS[account.id] = quota
    return quota


async def _run_warmup_iteration(db: Session, account: EmailAccount) -> None:
    """Execute the warmup sequence once for a given account."""

    for step in WARMUP_SEQUENCE:
        activity = await step(db, account=account)
        if step is send_test_email:
            await analyze_warmup_message(
                db,
                account,
                activity,
                sample="Warmup cadence verification email",
            )
    _DAILY_SENDS[account.id] += 1
    logger.info(
        "Completed warmup iteration for account %s (%s/%s)",
        account.email,
        _DAILY_SENDS[account.id],
        _DAILY_QUOTAS.get(account.id, "?"),
    )


async def warmup_cycle() -> None:
    """Background job that runs periodically to perform warmup iterations."""

    session = SessionLocal()
    try:
        accounts = session.query(EmailAccount).all()
        for account in accounts:
            quota = compute_daily_quota(account)
            sent = _DAILY_SENDS[account.id]
            if sent >= quota:
                continue
            await _run_warmup_iteration(session, account)
        if accounts:
            refresh_reputation_scores(session, accounts)
    finally:
        session.close()


def reset_daily_quota() -> None:
    """Reset counters at midnight so accounts can send a new warmup batch."""

    _DAILY_SENDS.clear()
    _DAILY_QUOTAS.clear()
    logger.info("Daily warmup quotas have been reset")


__all__ = [
    "WARMUP_SEQUENCE",
    "get_warmup_benefits",
    "mark_as_important",
    "mark_as_non_spam",
    "open_email",
    "reply_to_email",
    "maybe_reply",
    "send_test_email",
    "compute_daily_quota",
    "warmup_cycle",
    "reset_daily_quota",
]
