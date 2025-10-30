"""Simple CRUD helpers used across the application."""
from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models import User
from app.schemas import UserCreate


def create_user(db: Session, payload: UserCreate) -> User:
    """Create a new ``User`` instance without committing the transaction."""
    is_admin = getattr(payload, "is_admin", False)
    if not is_admin:
        # Support legacy ``is_superuser`` flag passed by instructions.
        is_admin = bool(getattr(payload, "is_superuser", False))
    user = User(
        email=payload.email,
        name=payload.name,
        hashed_password=get_password_hash(payload.password),
        is_active=getattr(payload, "is_active", True),
        is_admin=is_admin,
    )
    db.add(user)
    db.flush()
    return user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Fetch a user by email address."""
    return db.query(User).filter(User.email == email).first()
