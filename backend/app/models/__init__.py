"""Database models for Faceless Platform."""

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base


class UserRole(str, enum.Enum):
    """User roles."""
    ADMIN = "admin"
    CREATOR = "creator"
    VIEWER = "viewer"


class ContentStatus(str, enum.Enum):
    """Content processing status."""
    DRAFT = "draft"
    PROCESSING = "processing"
    READY = "ready"
    PUBLISHED = "published"
    FAILED = "failed"


class User(Base):
    """User model."""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.CREATOR)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    content_pieces = relationship("ContentPiece", back_populates="creator", cascade="all, delete-orphan")
    analytics = relationship("Analytics", back_populates="user", cascade="all, delete-orphan")
    monetization = relationship("Monetization", back_populates="user", cascade="all, delete-orphan")


class ContentPiece(Base):
    """Content piece model."""
    __tablename__ = "content_pieces"
    
    id = Column(String, primary_key=True, index=True)
    creator_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    script = Column(Text, nullable=False)
    template_id = Column(String, nullable=False)
    voice_id = Column(String, nullable=True)
    status = Column(Enum(ContentStatus), default=ContentStatus.DRAFT)
    duration = Column(Integer, nullable=True)  # in seconds
    video_url = Column(String, nullable=True)
    thumbnail_url = Column(String, nullable=True)
    metadata = Column(JSON, nullable=True)
    is_scheduled = Column(Boolean, default=False)
    scheduled_publish = Column(DateTime, nullable=True)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    creator = relationship("User", back_populates="content_pieces")
    analytics = relationship("Analytics", back_populates="content_piece", cascade="all, delete-orphan")


class Analytics(Base):
    """Analytics model."""
    __tablename__ = "analytics"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    content_id = Column(String, ForeignKey("content_pieces.id"), nullable=True)
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)
    ctr = Column(Float, default=0.0)  # Click-through rate
    conversion_rate = Column(Float, default=0.0)
    revenue = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="analytics")
    content_piece = relationship("ContentPiece", back_populates="analytics")


class Monetization(Base):
    """Monetization model."""
    __tablename__ = "monetization"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    stripe_customer_id = Column(String, nullable=True, unique=True)
    subscription_plan = Column(String, nullable=True)
    subscription_status = Column(String, default="inactive")
    total_earnings = Column(Float, default=0.0)
    pending_payout = Column(Float, default=0.0)
    paid_out = Column(Float, default=0.0)
    payout_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="monetization")


class Template(Base):
    """Video template model."""
    __tablename__ = "templates"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    thumbnail_url = Column(String, nullable=True)
    category = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    config = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Voice(Base):
    """Voice model for AI voice synthesis."""
    __tablename__ = "voices"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    language = Column(String, nullable=False)
    accent = Column(String, nullable=True)
    gender = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    provider = Column(String, default="elevenlabs")  # elevenlabs, openai, etc.
    provider_id = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
