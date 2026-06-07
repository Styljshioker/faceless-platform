"""Application configuration settings."""

from pydantic import BaseSettings, validator
from typing import List, Optional
import os


class Settings(BaseSettings):
    """Application settings."""
    
    # Basic settings
    PROJECT_NAME: str = "Faceless Platform"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost/faceless_platform"
    
    # Security
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # AI Services
    OPENAI_API_KEY: Optional[str] = None
    ELEVENLABS_API_KEY: Optional[str] = None
    REPLICATE_API_TOKEN: Optional[str] = None
    
    # Content Storage
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    S3_BUCKET_NAME: Optional[str] = None
    
    # External APIs
    YOUTUBE_API_KEY: Optional[str] = None
    TIKTOK_API_KEY: Optional[str] = None
    INSTAGRAM_API_KEY: Optional[str] = None
    
    # Redis (for caching and queues)
    REDIS_URL: str = "redis://localhost:6379"
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    
    @validator("ALLOWED_HOSTS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
