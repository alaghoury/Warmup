from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    email: EmailStr
    name: str = Field(..., alias="username")


class UserCreate(UserBase):
    password: str = Field(min_length=6)
    is_active: bool = True
    is_admin: bool = False
    is_superuser: bool | None = None


class UserOut(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True
