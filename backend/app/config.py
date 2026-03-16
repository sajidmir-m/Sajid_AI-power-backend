from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Support running from repo root or from within `backend/`
        env_file=("backend/.env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = Field(default="local", alias="APP_ENV")

    database_url: str = Field(
        default="postgresql+psycopg2://USER:PASSWORD@HOST:5432/DATABASE",
        alias="DATABASE_URL",
        description="Supabase Postgres URL (SQLAlchemy format).",
    )

    gemini_api_key: str | None = Field(default=None, alias="GEMINI_API_KEY")
    gemini_model: str = Field(
        default="gemini-1.5-flash",
        alias="GEMINI_MODEL",
        description="Gemini model name, e.g. gemini-1.5-flash or gemini-1.5-pro.",
    )

    # Comma-separated list in .env, or default local dev origins.
    cors_origins_raw: str = Field(
        default="http://localhost:3000,http://127.0.0.1:3000",
        alias="CORS_ORIGINS",
    )

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.cors_origins_raw.split(",") if o.strip()]


settings = Settings()

