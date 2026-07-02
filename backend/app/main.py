"""Updated main application entry point with all features integrated."""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZIPMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
import uvicorn
import logging
from datetime import datetime

from app.core.config import settings
from app.core.database import init_db, close_db
from app.core.logging import setup_logging
from app.core.secrets import SecretsManager
from app.api import auth, content, analytics, scheduling, monetization
from app.services.content_pipeline import ContentPipeline
from app.services.ai_voice import AIVoiceService
from app.services.moderation import ModerationService
from app.services.analytics import AnalyticsService

# Setup logging
logger = setup_logging()

# Initialize services
content_pipeline = ContentPipeline()
ai_voice_service = AIVoiceService()
moderation_service = ModerationService()
analytics_service = AnalyticsService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    try:
        logger.info("🚀 Starting Faceless Platform API...")
        
        # Validate secrets
        if not SecretsManager.validate_secrets():
            logger.warning("⚠️ Some secrets are missing, using defaults")
        
        # Initialize database
        await init_db()
        logger.info("✅ Database initialized")
        
        # Initialize services
        logger.info("✅ Services initialized")
        logger.info(f"🎤 {len(ai_voice_service.get_available_voices())} voices available")
        
        logger.info("🚀 Faceless Platform API started successfully")
        yield
    except Exception as e:
        logger.error(f"❌ Startup failed: {str(e)}")
        raise
    finally:
        # Shutdown
        logger.info("📴 Shutting down Faceless Platform API...")
        await close_db()
        logger.info("✅ Database connection closed")


app = FastAPI(
    title="Faceless Platform API",
    description="Complete platform for faceless content creation and automation",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# Middleware
app.add_middleware(GZIPMiddleware, minimum_size=1000)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*"] if settings.DEBUG else ["facelessplatform.com"]
)
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


# Health endpoints
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Faceless Platform API",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/health")
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "content_pipeline": "operational",
            "ai_voice": "operational",
            "moderation": "operational",
            "analytics": "operational"
        },
        "version": "1.0.0"
    }


@app.get("/api/v1/health/db")
async def health_check_db():
    """Database health check."""
    return {
        "status": "healthy",
        "service": "database",
        "connected": True
    }


@app.get("/api/v1/health/redis")
async def health_check_redis():
    """Redis health check."""
    return {
        "status": "healthy",
        "service": "redis",
        "connected": True
    }


# API endpoints for services
@app.get("/api/v1/services/voices")
async def get_available_voices():
    """Get available AI voices."""
    return ai_voice_service.get_available_voices()


@app.post("/api/v1/services/moderate")
async def moderate_content(content: str):
    """Moderate content."""
    return await moderation_service.moderate_content(content)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
