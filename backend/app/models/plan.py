"""Subscription plan model."""
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Float, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:  # pragma: no cover
    from .subscription import Subscription


class Plan(Base):
    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price_monthly: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    limits_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    subscriptions: Mapped[list["Subscription"]] = relationship("Subscription", back_populates="plan")
