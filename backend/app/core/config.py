"""
EduGuide Application Configuration

All settings are loaded from environment variables.
Environment variables can be provided via a .env file (see .env.example).

Design: Pydantic BaseSettings ensures type-safe, validated configuration
with zero hardcoded values. Each sub-phase extends this as new services
(PostgreSQL, Neo4j, Redis, etc.) are added.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application-wide settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # -------------------------------------------------------------------------
    # Application
    # -------------------------------------------------------------------------
    APP_NAME: str = "EduGuide API"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"  # development | staging | production
    DEBUG: bool = False

    # -------------------------------------------------------------------------
    # API
    # -------------------------------------------------------------------------
    API_V1_PREFIX: str = "/api/v1"

    # -------------------------------------------------------------------------
    # CORS
    # Origins are comma-separated in the env var, e.g.:
    # CORS_ORIGINS=http://localhost:5173,https://eduguide.kh
    # -------------------------------------------------------------------------
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    # -------------------------------------------------------------------------
    # Logging
    # -------------------------------------------------------------------------
    LOG_LEVEL: str = "INFO"  # DEBUG | INFO | WARNING | ERROR | CRITICAL

    # -------------------------------------------------------------------------
    # Databases
    # -------------------------------------------------------------------------
    DATABASE_URL: str
    NEO4J_URI: str
    NEO4J_USER: str
    NEO4J_PASSWORD: str
    REDIS_URL: str


# Module-level singleton — import this throughout the application.
settings = Settings()
