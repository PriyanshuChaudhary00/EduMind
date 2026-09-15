from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
import os
from app.routes.auth import router as auth_router
from app.routes.documents import router as documents_router
from app.routes.chat import router as chat_router
from app.routes.stats import router as stats_router

from sqlalchemy import text

# Ensure upload directory exists on startup
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# Create vector extension and database tables automatically
with engine.connect() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
    conn.commit()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="EduMind: AI-Powered Personalized Study Assistant API"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(auth_router)
app.include_router(documents_router, prefix=f"{settings.API_V1_STR}/documents", tags=["documents"])
app.include_router(documents_router, prefix="/documents", tags=["documents"])
app.include_router(chat_router, prefix=f"{settings.API_V1_STR}/chat", tags=["chat"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(stats_router, prefix=f"{settings.API_V1_STR}/stats", tags=["stats"])
app.include_router(stats_router, prefix="/stats", tags=["stats"])


@app.get("/")
def root():
    return {
        "message": "Welcome to EduMind API!",
        "version": settings.VERSION,
        "docs_url": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "EduMind Backend"}
