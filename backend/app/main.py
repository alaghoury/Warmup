"""FastAPI application exposing CRUD endpoints for users."""
from __future__ import annotations

from datetime import datetime
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from . import models


class UserCreate(BaseModel):
    """Payload used to create a new user."""

    name: str
    email: EmailStr


class UserRead(UserCreate):
    """Response model representing a persisted user."""

    id: int
    created_at: datetime

    class Config:
        from_attributes = True


app = FastAPI(title="Warmup API")

# Allow the React frontend (or any origin during development) to communicate with the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure database tables exist on startup.
Base.metadata.create_all(bind=engine)


@app.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)) -> models.User:
    """Insert a new user record into the database."""

    user = models.User(name=payload.name, email=payload.email)
    db.add(user)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        ) from exc
    db.refresh(user)
    return user


@app.get("/users", response_model=List[UserRead])
def list_users(db: Session = Depends(get_db)) -> List[models.User]:
    """Return all stored users."""

    return db.query(models.User).all()


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)) -> None:
    """Remove a user from the database if present."""

    user = db.get(models.User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()

