from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./warmup.db"
    JWT_SECRET: str = "devsecret_change_me"
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
    RUN_MIGRATIONS_ON_STARTUP: bool = True
    ADMIN_NAME: str = "mohammed"
    ADMIN_EMAIL: str = "mohammedalaghoury@gmail.com"
    ADMIN_PASSWORD: str = "Moh2611"


settings = Settings()
