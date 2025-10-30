from sqlalchemy.orm import Session
from app import models
from app.core.database import SessionLocal
from app.core.security import get_password_hash

def seed_superuser():
    db: Session = SessionLocal()
    try:
        superuser_email = "mohammedalaghoury@gmail.com"
        existing_user = db.query(models.User).filter(models.User.email == superuser_email).first()
        if not existing_user:
            user = models.User(
                username="mohammed",
                email=superuser_email,
                hashed_password=get_password_hash("Moh2611"),
                is_active=True,
                is_superuser=True,
            )
            db.add(user)
            db.commit()
            print("✅ Superuser 'mohammed' created successfully.")
        else:
            existing_user.is_superuser = True
            existing_user.is_active = True
            db.commit()
            print("ℹ️ Superuser already exists. Updated to ensure active & superuser privileges.")
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")
    finally:
        db.close()
