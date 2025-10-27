from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import User

app = FastAPI(title="Warmup API", version="0.1.0")


@app.on_event("startup")
def on_startup() -> None:
    """Create database tables when the application starts."""

    Base.metadata.create_all(bind=engine)


class UserCreate(BaseModel):
    name: str
    email: str


class UserRead(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True


@app.get("/", summary="Service heartbeat")
def read_root() -> dict[str, str]:
    """Return a simple payload confirming that the API is running."""

    return {"message": "Warmup API OK"}


@app.get("/health", summary="Health check")
def health_check() -> dict[str, str]:
    """Return a health indicator for monitoring purposes."""

    return {"status": "healthy"}


@app.post("/api/users", response_model=UserRead, status_code=201, summary="Create user")
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    """Create a new user and persist it to the database."""

    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    try:
        db.commit()
    except IntegrityError as exc:  # pragma: no cover - defensive programming
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered") from exc
    db.refresh(db_user)
    return db_user


@app.get("/api/users", response_model=list[UserRead], summary="List users")
def list_users(db: Session = Depends(get_db)) -> list[User]:
    """Return all users stored in the database."""

    users = db.query(User).all()
    return users


app.mount("/app", StaticFiles(directory="app/static", html=True), name="app_static")


@app.get("/ui", include_in_schema=False)
def ui_redirect() -> RedirectResponse:
    """Redirect to the static user interface."""

    return RedirectResponse(url="/app/index.html")
