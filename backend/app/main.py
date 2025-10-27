from fastapi import FastAPI
from .config import settings
from .database import Base, engine
from .api.v1.users import router as users_router
from .api.v1.accounts import router as accounts_router
from .api.v1.tasks import router as tasks_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os

app = FastAPI(title=settings.APP_NAME, version="0.1.0")

# إنشاء الجداول مبدئيًا (هنستخدم Alembic بعدين)
Base.metadata.create_all(bind=engine)

api = settings.API_PREFIX
app.include_router(users_router, prefix=api)
app.include_router(accounts_router, prefix=api)
app.include_router(tasks_router, prefix=api)

# static mount (React لاحقًا)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(static_dir):
    app.mount("/app", StaticFiles(directory=static_dir, html=True), name="app")

    @app.get("/ui")
    def ui_redirect():
        return RedirectResponse(url="/app/index.html")


@app.get("/")
def health():
    return {"message": "Warmup SaaS OK"}
