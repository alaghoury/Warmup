from __future__ import annotations

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    DATABASE_URL: str = Field("sqlite:///./app.db", alias="DATABASE_URL")
    SECRET_KEY: str = Field("dev_secret_change_me", alias="SECRET_KEY")
    JWT_ALG: str = Field("HS256", alias="JWT_ALG")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    CORS_ORIGINS: list[str] | str = Field(
        default_factory=lambda: [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        alias="CORS_ORIGINS",
    )
    RUN_MIGRATIONS_ON_STARTUP: bool = Field(True, alias="RUN_MIGRATIONS_ON_STARTUP")
    SEED_SUPERUSER: bool = Field(True, alias="SEED_SUPERUSER")
    SUPERUSER_NAME: str = Field("mohammed", alias="SUPERUSER_NAME")
    SUPERUSER_EMAIL: str = Field("mohammedalaghoury@gmail.com", alias="SUPERUSER_EMAIL")
    SUPERUSER_PASSWORD: str = Field("Moh2611", alias="SUPERUSER_PASSWORD")
    SPAM_CHECK_API_URL: str | None = Field(None, alias="SPAM_CHECK_API_URL")
    SPAM_CHECK_API_KEY: str | None = Field(None, alias="SPAM_CHECK_API_KEY")
    REPUTATION_ALERT_THRESHOLD: float = Field(15.0, alias="REPUTATION_ALERT_THRESHOLD")

    class Config:
        env_file = ".env"

    @field_validator("CORS_ORIGINS", mode="after")
    @classmethod
    def _normalize_cors(cls, value: list[str] | str) -> list[str]:
        """Allow comma-separated strings or wildcard."""
        if isinstance(value, list):
            return value
        raw = value.strip()
        if raw == "*":
            return ["*"]
        return [origin.strip() for origin in raw.split(",") if origin.strip()]

    @property
    def JWT_SECRET(self) -> str:  # pragma: no cover - compatibility shim
        """Expose SECRET_KEY under the legacy name expected elsewhere."""
        return self.SECRET_KEY

    # Backwards compatibility for previous settings attributes used in tests/code.
    @property
    def ADMIN_NAME(self) -> str:  # pragma: no cover - backward compat
        return self.SUPERUSER_NAME

    @property
    def ADMIN_EMAIL(self) -> str:  # pragma: no cover - backward compat
        return self.SUPERUSER_EMAIL

    @property
    def ADMIN_PASSWORD(self) -> str:  # pragma: no cover - backward compat
        return self.SUPERUSER_PASSWORD


settings = Settings()
