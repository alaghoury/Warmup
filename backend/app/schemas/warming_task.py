from pydantic import BaseModel


class WarmingTaskCreate(BaseModel):
    account_id: int
    kind: str = "email"


class WarmingTaskRead(WarmingTaskCreate):
    id: int
    state: str
