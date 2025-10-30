from fastapi import FastAPI

app = FastAPI()

import logging
from typing import Iterable

from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError

from app import cli, crud
from app.config import settings
from app.core.security import get_password_hash, verify_password
from app.database import SessionLocal
from app.models import Plan, User
from app.routes import admin, analytics, auth, subscriptions, users
from app.schemas import UserCreate

app.title = "Warmup SaaS"
app.openapi_url = "/openapi.json"

cors_origins: Iterable[str] = settings.CORS_ORIGINS
allow_credentials = True
if list(cors_origins) == ["*"]:
    allow_credentials = False

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(cors_origins),
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    if settings.RUN_MIGRATIONS_ON_STARTUP:
        try:
            cli.upgrade()
        except Exception as exc:  # pragma: no cover - startup failure should be visible in logs
            logging.getLogger(__name__).exception(
                "Failed to apply database migrations: %s", exc
            )
            raise
    with SessionLocal() as db:
        if not db.query(Plan).first():
            plans = [
                {
                    "slug": "free",
                    "name": "Free",
                    "price_monthly": 0,
                    "limits_json": {
                        "max_users": 1,
                        "max_actions": 100,
                        "max_api_calls": 1000,
                    },
                },
                {
                    "slug": "starter",
                    "name": "Starter",
                    "price_monthly": 9,
                    "limits_json": {
                        "max_users": 3,
                        "max_actions": 1000,
                        "max_api_calls": 10000,
                    },
                },
                {
                    "slug": "professional",
                    "name": "Professional",
                    "price_monthly": 29,
                    "limits_json": {
                        "max_users": 10,
                        "max_actions": 5000,
                        "max_api_calls": 50000,
                    },
                },
                {
                    "slug": "enterprise",
                    "name": "Enterprise",
                    "price_monthly": 99,
                    "limits_json": {
                        "max_users": 100,
                        "max_actions": 50000,
                        "max_api_calls": 500000,
                    },
                },
            ]
            for plan in plans:
                db.add(Plan(**plan))
            db.commit()


@app.on_event("startup")
def create_default_admin() -> None:
    db = SessionLocal()
    try:
        admin_email = settings.ADMIN_EMAIL
        existing = db.query(User).filter(User.email == admin_email).first()
        if not existing:
            try:
                user_in = UserCreate(
                    email=admin_email,
                    password=settings.ADMIN_PASSWORD,
                    name=settings.ADMIN_NAME,
                    is_admin=True,
                    is_active=True,
                )
                user = crud.create_user(db, user_in)
                user.is_admin = True
                user.is_active = True
                db.commit()
                print("✅ Default admin user created successfully.")
            except IntegrityError:
                db.rollback()
        else:
            updated = False
            if not existing.is_admin:
                existing.is_admin = True
                updated = True
            if not existing.is_active:
                existing.is_active = True
                updated = True
            if not verify_password(settings.ADMIN_PASSWORD, existing.hashed_password):
                existing.hashed_password = get_password_hash(settings.ADMIN_PASSWORD)
                updated = True
            if existing.name != settings.ADMIN_NAME:
                existing.name = settings.ADMIN_NAME
                updated = True
            if updated:
                db.add(existing)
                db.commit()
    finally:
        db.close()


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(subscriptions.router)
app.include_router(analytics.router)
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])


@app.get("/api/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
