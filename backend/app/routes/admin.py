"""Administrative endpoints."""
from __future__ import annotations

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.deps import get_current_admin, get_db
from app.models import User
from app.schemas import AdminStats, UserOut

router = APIRouter(tags=["admin"])


@router.get("/users", response_model=list[UserOut])
def list_users(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
) -> list[User]:
    return db.query(User).order_by(User.created_at.desc()).all()


@router.post("/users/{user_id}/deactivate", status_code=status.HTTP_200_OK)
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
) -> dict[str, bool]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.is_active = False
    db.commit()
    return {"ok": True}


@router.post("/users/{user_id}/activate", status_code=status.HTTP_200_OK)
def activate_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
) -> dict[str, bool]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.is_active = True
    db.commit()
    return {"ok": True}


@router.get("/stats", response_model=AdminStats)
def stats(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
) -> dict[str, int]:
    total_users = db.query(func.count(User.id)).scalar() or 0
    active_users = db.query(func.count(User.id)).filter(User.is_active.is_(True)).scalar() or 0
    since = datetime.utcnow() - timedelta(days=7)
    recent_signups = (
        db.query(func.count(User.id))
        .filter(User.created_at >= since)
        .scalar()
        or 0
    )
    return {
        "total_users": total_users,
        "active_users": active_users,
        "recent_signups": recent_signups,
    }
