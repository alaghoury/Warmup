from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from ..database import Base


class Account(Base):
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    label: Mapped[str] = mapped_column(String(120), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="active")
