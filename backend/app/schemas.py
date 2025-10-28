from typing import Any

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    password: str = Field(min_length=6)


class UserOut(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PlanOut(BaseModel):
    id: int
    slug: str
    name: str
    price_monthly: float
    limits_json: dict[str, Any]

    class Config:
        from_attributes = True


class SubscriptionOut(BaseModel):
    id: int
    status: str
    plan: PlanOut

    class Config:
        from_attributes = True


class UsageSummary(BaseModel):
    used_api_calls: int
    limit_api_calls: int
    remaining_api_calls: int
