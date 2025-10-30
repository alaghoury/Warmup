import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import cli
from app.config import settings
from app.core.security import get_password_hash, verify_password
from app.database import SessionLocal
from app.models import Plan, User
from app.routes import admin, analytics, auth, subscriptions, users

app = FastAPI(title="Warmup SaaS", openapi_url="/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    if settings.RUN_MIGRATIONS_ON_STARTUP:
        try:
            cli.upgrade()
        except Exception as exc:  # pragma: no cover - startup failure should be visible in logs
            logging.getLogger(__name__).exception("Failed to apply database migrations: %s", exc)
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
        if settings.SEED_SUPERUSER:
            admin = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()
            if not admin:
                admin = User(
                    name=settings.ADMIN_NAME,
                    email=settings.ADMIN_EMAIL,
                    hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
                    is_admin=True,
                    is_active=True,
                )
                db.add(admin)
                db.commit()
            else:
                updated = False
                if admin.name != settings.ADMIN_NAME:
                    admin.name = settings.ADMIN_NAME
                    updated = True
                if not admin.is_admin:
                    admin.is_admin = True
                    updated = True
                if not admin.is_active:
                    admin.is_active = True
                    updated = True
                if not verify_password(settings.ADMIN_PASSWORD, admin.hashed_password):
                    admin.hashed_password = get_password_hash(settings.ADMIN_PASSWORD)
                    updated = True
                if updated:
                    db.add(admin)
                    db.commit()


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(subscriptions.router)
app.include_router(analytics.router)
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])


@app.get("/api/health")
def health() -> dict[str, bool]:
    return {"ok": True}
