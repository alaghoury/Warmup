from typing import Any

from pydantic import BaseModel


class SubscriptionCreate(BaseModel):
    plan_slug: str


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
