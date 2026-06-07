"""Main FastAPI application for Faceless Platform."""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
import uvicorn

from app.core.config import settings
from app.core.database import init_db
from app.api import auth, content, analytics, scheduling, monetization
from app.services.content_pipeline import ContentPipeline
from app.services.ai_voice import AIVoiceService
from app.services.moderation import ModerationService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    await init_db()
    print("🚀 Faceless Platform API started")
    yield
    # Shutdown
    print("📴 Faceless Platform API stopped")


app = FastAPI(
    title="Faceless Platform API",
    description="Complete platform for faceless content creation and automation",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(content.router, prefix="/api/v1/content", tags=["Content Creation"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])
app.include_router(scheduling.router, prefix="/api/v1/scheduling", tags=["Scheduling"])
app.include_router(monetization.router, prefix="/api/v1/monetization", tags=["Monetization"])


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "Faceless Platform API",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "services": {
            "content_pipeline": "operational",
            "ai_voice": "operational",
            "moderation": "operational",
            "analytics": "operational"
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if settings.ENVIRONMENT == "development" else False
    )
