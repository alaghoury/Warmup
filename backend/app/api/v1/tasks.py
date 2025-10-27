from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...database import get_db
from ...models.warming_task import WarmingTask
from ...schemas.warming_task import WarmingTaskCreate, WarmingTaskRead


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[WarmingTaskRead])
def list_tasks(db: Session = Depends(get_db)):
    return db.query(WarmingTask).all()


@router.post("", response_model=WarmingTaskRead)
def create_task(payload: WarmingTaskCreate, db: Session = Depends(get_db)):
    obj = WarmingTask(account_id=payload.account_id, kind=payload.kind)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
