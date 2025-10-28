from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, SessionLocal, engine
from app.models import Plan
from app.routes import analytics, auth, subscriptions, users

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
    Base.metadata.create_all(bind=engine)
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


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(subscriptions.router)
app.include_router(analytics.router)


@app.get("/api/health")
def health() -> dict[str, bool]:
    return {"ok": True}
