from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from ...database import get_db
from ...models import WarmingTask
from ...schemas.warming_task import WarmingTaskCreate, WarmingTaskRead
from ...worker import queue, warming_job

router = APIRouter(prefix="/tasks", tags=["tasks"])


class QueueRequest(BaseModel):
    email: EmailStr


class QueueResponse(BaseModel):
    job_id: str
    status: str


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


@router.post("/queue", response_model=QueueResponse)
def queue_warming_job(payload: QueueRequest):
    job = queue.enqueue(warming_job, payload.email)
    return QueueResponse(job_id=job.id, status=job.get_status())
