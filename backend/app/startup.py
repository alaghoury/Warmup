import os
import subprocess
from sqlalchemy.orm import Session

from app import models
from app.config import settings
from app.core.database import Base, SessionLocal, engine
from app.core.security import get_password_hash


def apply_migrations() -> None:
    alembic_path = "/app/alembic.ini"
    if not os.path.exists(alembic_path):
        print(
            f"⚠️ Alembic config not found at {alembic_path}, running fallback SQLAlchemy create_all()"
        )
        Base.metadata.create_all(bind=engine)
        return

    try:
        print("🧱 Applying Alembic migrations...")
        subprocess.run(["alembic", "-c", alembic_path, "upgrade", "head"], check=True)
        print("✅ Alembic migrations applied successfully.")
    except subprocess.CalledProcessError as exc:  # pragma: no cover - best effort logging
        print(f"❌ Alembic migration failed: {exc}. Running fallback create_all().")
        Base.metadata.create_all(bind=engine)


def seed_superuser() -> None:
    db: Session = SessionLocal()
    try:
        superuser_email = settings.SUPERUSER_EMAIL
        existing = db.query(models.User).filter(models.User.email == superuser_email).first()

        if not existing:
            user = models.User(
                username=settings.SUPERUSER_NAME,
                email=superuser_email,
                hashed_password=get_password_hash(settings.SUPERUSER_PASSWORD),
                is_active=True,
                is_superuser=True,
            )
            db.add(user)
            db.commit()
            print(f"✅ Superuser '{settings.SUPERUSER_NAME}' created successfully.")
        else:
            existing.is_superuser = True
            existing.is_active = True
            db.commit()
            print(f"ℹ️ Superuser {settings.SUPERUSER_EMAIL} already exists and was updated.")
    except Exception as exc:  # pragma: no cover - best effort logging
        print(f"❌ Error creating superuser: {exc}")
    finally:
        db.close()
