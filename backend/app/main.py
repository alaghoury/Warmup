from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routes import admin, analytics, auth, subscriptions, users
from app.routers import warmup
from app.startup import apply_migrations, seed_superuser

app = FastAPI(title="Warmup SaaS")

allow_credentials = "*" not in settings.CORS_ORIGINS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    print("🚀 Application starting...")
    if settings.RUN_MIGRATIONS_ON_STARTUP:
        apply_migrations()
    if settings.SEED_SUPERUSER:
        seed_superuser()


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(subscriptions.router)
app.include_router(analytics.router)
app.include_router(admin.router, prefix="/api/v1/admin")
app.include_router(warmup.router, prefix="/api/warmup")


@app.get("/", include_in_schema=False)
def root() -> dict[str, str]:
    return {"status": "ok", "message": "Warmup SaaS"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/v1/health")
def api_health_check() -> dict[str, str]:
    return {"status": "ok"}


static_dir = Path(__file__).parent / "static"
if (static_dir / "index.html").exists():
    app.mount("/app", StaticFiles(directory=static_dir, html=True), name="frontend")

    @app.get("/ui", include_in_schema=False)
    def ui_redirect() -> RedirectResponse:
        return RedirectResponse(url="/app/index.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
