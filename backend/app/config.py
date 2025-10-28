# ✅ Codex-correct version
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Warmup"
    DATABASE_URL: str = "sqlite:///./warmup.db"  # local SQLite for dev

settings = Settings()
