"""User model definition."""
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import DeclarativeMeta as BaseModel  # type: ignore

from app.database import Base

# Alias kept for compatibility with instructions expecting a ``BaseModel`` symbol.
BaseModel = Base  # type: ignore

if TYPE_CHECKING:  # pragma: no cover - circular import guard for type checkers
    from .subscription import Subscription
    from .email_account import EmailAccount


class User(Base):
    """Represents an authenticated Warmup user."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    subscriptions: Mapped[list["Subscription"]] = relationship(
        "Subscription", back_populates="user", cascade="all, delete-orphan"
    )
    email_accounts: Mapped[list["EmailAccount"]] = relationship(
        "EmailAccount", back_populates="user", cascade="all, delete-orphan"
    )

    @property
    def username(self) -> str:
        """Alias for compatibility with instructions expecting a ``username`` field."""

        return self.name

    @username.setter
    def username(self, value: str) -> None:
        self.name = value

    @property
    def is_superuser(self) -> bool:
        """Mirror ``is_admin`` to satisfy interfaces that expect ``is_superuser``."""

        return self.is_admin

    @is_superuser.setter
    def is_superuser(self, value: bool) -> None:
        self.is_admin = value
