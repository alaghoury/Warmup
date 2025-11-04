"""Reputation monitoring endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps import get_current_user, get_db
from app.schemas.reputation import ReputationStats
from app.services.reputation_service import get_reputation_stats

router = APIRouter(prefix="/api/v1/reputation", tags=["reputation"])


@router.get("/stats", response_model=ReputationStats)
def reputation_stats(db: Session = Depends(get_db), current=Depends(get_current_user)) -> ReputationStats:
    data = get_reputation_stats(db, current.id)
    return ReputationStats(**data)
