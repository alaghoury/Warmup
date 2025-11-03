from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps import get_current_user, get_db
from app.models import Plan, Subscription, UsageLog
from app.schemas import PlanOut, SubscriptionOut, UsageSummary

router = APIRouter(prefix="/api/v1/subscriptions", tags=["subscriptions"])


@router.get("/plans", response_model=list[PlanOut])
def get_plans(db: Session = Depends(get_db)):
    return db.query(Plan).filter(Plan.is_active.is_(True)).all()


@router.get("/me", response_model=SubscriptionOut | None)
def get_my_subscription(
    db: Session = Depends(get_db), current=Depends(get_current_user)
):
    return (
        db.query(Subscription)
        .filter(Subscription.user_id == current.id, Subscription.status == "active")
        .first()
    )


@router.post("/checkout")
def checkout(plan_slug: str, db: Session = Depends(get_db), current=Depends(get_current_user)):
    plan = (
        db.query(Plan)
        .filter(Plan.slug == plan_slug, Plan.is_active.is_(True))
        .first()
    )
    if not plan:
        return {"ok": False, "message": "plan not found"}
    db.query(Subscription).filter(
        Subscription.user_id == current.id, Subscription.status == "active"
    ).update({"status": "canceled"})
    subscription = Subscription(user_id=current.id, plan_id=plan.id, status="active")
    db.add(subscription)
    db.commit()
    return {"ok": True, "message": "subscription activated", "plan": plan.slug}


@router.get("/usage", response_model=UsageSummary)
def usage(db: Session = Depends(get_db), current=Depends(get_current_user)):
    subscription = (
        db.query(Subscription)
        .filter(Subscription.user_id == current.id, Subscription.status == "active")
        .first()
    )
    plan = (
        subscription.plan
        if subscription
        else db.query(Plan).filter(Plan.slug == "free").first()
    )
    limits = plan.limits_json if plan and plan.limits_json else {}
    limit_api = int(limits.get("max_api_calls", 1000))
    used_api = (
        db.query(UsageLog)
        .filter(UsageLog.user_id == current.id, UsageLog.kind == "api_call")
        .count()
    )
    return {
        "used_api_calls": used_api,
        "limit_api_calls": limit_api,
        "remaining_api_calls": max(0, limit_api - used_api),
    }
