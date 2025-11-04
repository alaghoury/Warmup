"""Reputation monitoring helpers."""
from __future__ import annotations

import logging
from collections import defaultdict
from datetime import date
from typing import Iterable, Sequence

from sqlalchemy.orm import Session

from app.config import settings
from app.models import EmailAccount, ReputationHistory
from app.services.alert_service import notify_reputation_drop
from app.services.spam_check_service import summarize_user_scores

logger = logging.getLogger(__name__)


def _calculate_score(spam_scores: Sequence[float]) -> float:
    """Convert spam scores into a 0-100 reputation rating."""

    if not spam_scores:
        return 100.0
    average = sum(spam_scores) / len(spam_scores)
    score = max(0.0, min(100.0, 100.0 - average * 12))
    return round(score, 2)


def refresh_account_reputation(db: Session, account: EmailAccount) -> ReputationHistory:
    """Calculate and persist today's reputation score for an account."""

    grouped = summarize_user_scores(db, [account.id])
    messages = grouped.get(account.id, [])
    spam_scores = [msg.spam_score for msg in messages if msg.spam_score is not None]
    score = _calculate_score(spam_scores)
    avg_spam = round(sum(spam_scores) / len(spam_scores), 2) if spam_scores else None

    today = date.today()
    existing = (
        db.query(ReputationHistory)
        .filter(ReputationHistory.account_id == account.id)
        .order_by(ReputationHistory.recorded_at.desc())
        .first()
    )

    previous_score = existing.score if existing else None
    if existing and existing.recorded_at.date() == today:
        entry = existing
        entry.score = score
        entry.spam_score = avg_spam
        entry.details = {"messages": len(messages)}
    else:
        entry = ReputationHistory(
            account_id=account.id,
            score=score,
            spam_score=avg_spam,
            details={"messages": len(messages)},
        )
        db.add(entry)

    db.commit()
    db.refresh(entry)

    threshold = settings.REPUTATION_ALERT_THRESHOLD
    if (
        previous_score is not None
        and previous_score - entry.score > threshold
    ):
        notify_reputation_drop(account, entry.score, previous_score)

    return entry


def refresh_reputation_scores(db: Session, accounts: Iterable[EmailAccount]) -> list[ReputationHistory]:
    """Update reputation metrics for all provided accounts."""

    results: list[ReputationHistory] = []
    for account in accounts:
        results.append(refresh_account_reputation(db, account))
    return results


def get_reputation_stats(db: Session, user_id: int) -> dict[str, object]:
    """Return history and alert metadata for accounts belonging to the user."""

    records = (
        db.query(ReputationHistory)
        .join(EmailAccount, EmailAccount.id == ReputationHistory.account_id)
        .filter(EmailAccount.user_id == user_id)
        .order_by(ReputationHistory.recorded_at.asc())
        .all()
    )
    if not records:
        return {
            "history": [],
            "latest": None,
            "threshold": settings.REPUTATION_ALERT_THRESHOLD,
            "alert": False,
        }

    account_map = {
        account.id: account
        for account in db.query(EmailAccount).filter(EmailAccount.user_id == user_id).all()
    }

    history: list[dict[str, object]] = []
    per_account: dict[int, list[ReputationHistory]] = defaultdict(list)
    for record in records:
        per_account[record.account_id].append(record)
        account = account_map.get(record.account_id)
        history.append(
            {
                "account_id": record.account_id,
                "account_email": account.email if account else None,
                "score": record.score,
                "spam_score": record.spam_score,
                "recorded_at": record.recorded_at,
            }
        )

    alert_threshold = settings.REPUTATION_ALERT_THRESHOLD
    alert = False
    for account_id, points in per_account.items():
        if len(points) < 2:
            continue
        previous, latest = points[-2], points[-1]
        if previous.score - latest.score > alert_threshold:
            alert = True
            break

    latest_point = max(history, key=lambda item: item["recorded_at"])
    return {
        "history": history,
        "latest": latest_point,
        "threshold": alert_threshold,
        "alert": alert,
    }


__all__ = [
    "refresh_reputation_scores",
    "refresh_account_reputation",
    "get_reputation_stats",
]
