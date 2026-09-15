from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROJECT_NAME: str = "EduMind API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Database: Supports SQLite (for immediate local dev) or PostgreSQL (Neon, Supabase, Docker)
    DATABASE_URL: str = "sqlite:///./edumind.db"

    # Security & JWT Configuration
    JWT_SECRET_KEY: str = "edumind-insecure-dev-secret-key-change-in-production-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # CORS origins for frontend access
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]


settings = Settings()
