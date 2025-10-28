# ✅ Codex-correct version
from pathlib import Path
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .config import settings
from .database import Base, engine, get_db
from .models import User

# ---- Pydantic Schemas (v2) ----
class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr

# ---- App ----
app = FastAPI(title=settings.APP_NAME)

# CORS (allow Vite dev server)
origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup if not exist
Base.metadata.create_all(bind=engine)

# Mount static files
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", include_in_schema=False)
def root():
    return {"app": settings.APP_NAME, "ok": True}

@app.get("/ui", include_in_schema=False)
def serve_ui():
    return RedirectResponse(url="/static/index.html")

# ---- Users Endpoints ----
@app.get("/api/health", include_in_schema=False)
def api_health():
    return {"status": "ok", "app": settings.APP_NAME}


@app.get("/api/users", response_model=List[UserRead])
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.id.desc()).all()
    return users

@app.post("/api/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    u = User(name=payload.name, email=str(payload.email))
    db.add(u)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )
    db.refresh(u)
    return u

@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.id == user_id).first()
    if not u:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(u)
    db.commit()
    return
