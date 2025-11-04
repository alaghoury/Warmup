from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps import get_current_user, get_db
from app.models import UsageLog, User
from app.schemas import AnalyticsSummary

router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])


@router.get("/summary", response_model=AnalyticsSummary)
def summary(db: Session = Depends(get_db), current=Depends(get_current_user)):
    total_users = db.query(User).count()
    total_calls = db.query(UsageLog).count()
    return {"total_users": total_users, "total_api_calls": total_calls}
