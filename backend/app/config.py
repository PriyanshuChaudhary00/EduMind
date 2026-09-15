from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROJECT_NAME: str = "EduMind API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: str = "sqlite:///./edumind.db"

    # Security & JWT
    JWT_SECRET_KEY: str = "edumind-insecure-dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://edu-mind-priyanshu.vercel.app",  # update after Vercel deploy
        "https://*.vercel.app",
    ]

    # Google Gemini AI
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # RAG Configuration
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    MAX_RETRIEVED_CHUNKS: int = 5
    SIMILARITY_THRESHOLD: float = 0.7

    # File Upload
    MAX_FILE_SIZE_MB: int = 20
    UPLOAD_DIR: str = "uploads"


settings = Settings()
