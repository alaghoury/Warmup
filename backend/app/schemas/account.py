from pydantic import BaseModel


class AccountCreate(BaseModel):
    label: str


class AccountRead(AccountCreate):
    id: int
    status: str
