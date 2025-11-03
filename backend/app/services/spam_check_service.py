"""Spam scoring helpers using external services when available."""
from __future__ import annotations

import logging
import random
from datetime import datetime, timedelta
from typing import Any

import httpx
from sqlalchemy.orm import Session

from app.config import settings
from app.models import EmailAccount, WarmupActivity, WarmupMessage

logger = logging.getLogger(__name__)

_DEFAULT_TIMEOUT = 15.0
_FALLBACK_MIN = 0.1
_FALLBACK_MAX = 4.0


async def _request_external_score(domain: str) -> dict[str, Any] | None:
    """Call a configured spam-check API if available."""

    if not settings.SPAM_CHECK_API_URL:
        return None

    payload = {"domain": domain}
    headers = {"Accept": "application/json"}
    if settings.SPAM_CHECK_API_KEY:
        headers["Authorization"] = f"Bearer {settings.SPAM_CHECK_API_KEY}"

    try:
        async with httpx.AsyncClient(timeout=_DEFAULT_TIMEOUT) as client:
            response = await client.post(settings.SPAM_CHECK_API_URL, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
    except Exception as exc:  # pragma: no cover - network failures are non-deterministic
        logger.warning("Spam check request failed: %s", exc)
        return None

    score = float(data.get("score", 0.0))
    reason = data.get("reason", "external_report")
    return {
        "score": score,
        "reason": reason,
        "provider": settings.SPAM_CHECK_API_URL,
        "raw": data,
    }


def _fallback_score(domain: str) -> dict[str, Any]:
    """Generate a deterministic fallback spam score when no API is available."""

    random.seed(domain)
    score = round(random.uniform(_FALLBACK_MIN, _FALLBACK_MAX), 2)
    return {
        "score": score,
        "reason": "simulated",
        "provider": "fallback",
    }


async def analyze_warmup_message(
    db: Session,
    account: EmailAccount,
    activity: WarmupActivity | None = None,
    sample: str | None = None,
) -> WarmupMessage:
    """Fetch a spam score for the account's domain and persist it."""

    domain = account.email.split("@")[-1]
    report = await _request_external_score(domain)
    if report is None:
        report = _fallback_score(domain)

    details = {
        "reason": report.get("reason"),
        "provider": report.get("provider"),
    }
    if sample:
        details["sample"] = sample
    if "raw" in report:
        details["raw"] = report["raw"]

    message = WarmupMessage(
        account_id=account.id,
        activity_id=activity.id if activity else None,
        domain=domain,
        spam_score=float(report.get("score", 0.0)),
        spam_details=details,
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    logger.info("Recorded spam score %.2f for %s", message.spam_score or 0.0, domain)
    return message


def summarize_domain_scores(db: Session, domain: str) -> dict[str, Any]:
    """Summarise spam score metrics for a domain."""

    query = (
        db.query(WarmupMessage)
        .filter(WarmupMessage.domain == domain)
        .order_by(WarmupMessage.created_at.desc())
    )
    messages = query.limit(50).all()
    if not messages:
        return {
            "count": 0,
            "average_score": None,
            "latest_score": None,
            "last_checked_at": None,
        }

    scores = [msg.spam_score for msg in messages if msg.spam_score is not None]
    avg = round(sum(scores) / len(scores), 2) if scores else None
    latest = messages[0]
    return {
        "count": len(messages),
        "average_score": avg,
        "latest_score": latest.spam_score,
        "last_checked_at": latest.created_at,
        "provider": latest.spam_details.get("provider") if latest.spam_details else None,
    }


def summarize_user_scores(db: Session, account_ids: list[int], days: int = 7) -> dict[int, list[WarmupMessage]]:
    """Return recent warmup messages grouped by account id."""

    if not account_ids:
        return {}
    cutoff = datetime.utcnow() - timedelta(days=days)
    rows = (
        db.query(WarmupMessage)
        .filter(WarmupMessage.account_id.in_(account_ids))
        .filter(WarmupMessage.created_at >= cutoff)
        .order_by(WarmupMessage.created_at.asc())
        .all()
    )

    grouped: dict[int, list[WarmupMessage]] = {account_id: [] for account_id in account_ids}
    for row in rows:
        if row.account_id is None:
            continue
        grouped.setdefault(row.account_id, []).append(row)
    return grouped


__all__ = [
    "analyze_warmup_message",
    "summarize_domain_scores",
    "summarize_user_scores",
]
