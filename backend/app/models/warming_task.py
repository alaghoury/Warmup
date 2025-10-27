from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from ..database import Base


class WarmingTask(Base):
    __tablename__ = "warming_tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    account_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    kind: Mapped[str] = mapped_column(String(32), default="email")
    state: Mapped[str] = mapped_column(String(32), default="queued")
