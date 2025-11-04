"""Warmup automation API endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps import get_current_user, get_db
from app.models import WarmupActivity
from app.schemas import WarmupActivityRead, WarmupInsight
from app.services.warmup_service import WARMUP_SEQUENCE, get_warmup_benefits

router = APIRouter(tags=["warmup"])


@router.get("/status", response_model=list[WarmupActivityRead])
def warmup_status(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
) -> list[WarmupActivity]:
    """Return the most recent warmup activities (up to 50)."""

    activities = (
        db.query(WarmupActivity)
        .order_by(WarmupActivity.timestamp.desc())
        .limit(50)
        .all()
    )
    return activities


@router.post("/start", response_model=list[WarmupActivityRead])
async def start_warmup(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
) -> list[WarmupActivity]:
    """Execute the warmup automation steps sequentially."""

    results: list[WarmupActivity] = []
    for step in WARMUP_SEQUENCE:
        activity = await step(db)
        results.append(activity)
    return results


@router.get("/insights", response_model=list[WarmupInsight])
def warmup_insights(
    current_user=Depends(get_current_user),
) -> list[WarmupInsight]:
    """Expose marketing insights that describe the warmup automation benefits."""

    return get_warmup_benefits()
