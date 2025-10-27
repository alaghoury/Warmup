from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Warmup SaaS"
    API_PREFIX: str = "/api/v1"
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@db:5432/warmup"
    REDIS_URL: str = "redis://redis:6379/0"
    ENV: str = "dev"

    class Config:
        env_file = ".env"


settings = Settings()
