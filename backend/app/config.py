from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    DATABASE_URL: str = Field("sqlite:///./app.db", alias="DATABASE_URL")
    SECRET_KEY: str = Field("dev_secret_change_me", alias="SECRET_KEY")
    JWT_ALG: str = Field("HS256", alias="JWT_ALG")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    CORS_ORIGINS: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        alias="CORS_ORIGINS",
    )
    RUN_MIGRATIONS_ON_STARTUP: bool = Field(True, alias="RUN_MIGRATIONS_ON_STARTUP")
    SEED_SUPERUSER: bool = Field(True, alias="SEED_SUPERUSER")
    ADMIN_NAME: str = Field("mohammed", alias="ADMIN_NAME")
    ADMIN_EMAIL: str = Field("mohammedalaghoury@gmail.com", alias="ADMIN_EMAIL")
    ADMIN_PASSWORD: str = Field("Moh2611", alias="ADMIN_PASSWORD")

    class Config:
        env_file = ".env"

    @property
    def JWT_SECRET(self) -> str:  # pragma: no cover - compatibility shim
        """Expose SECRET_KEY under the legacy name expected elsewhere."""
        return self.SECRET_KEY


settings = Settings()
