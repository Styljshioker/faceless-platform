"""Pydantic schemas for request/response validation."""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    CREATOR = "creator"
    VIEWER = "viewer"


class ContentStatus(str, Enum):
    DRAFT = "draft"
    PROCESSING = "processing"
    READY = "ready"
    PUBLISHED = "published"
    FAILED = "failed"


# ============= User Schemas =============
class UserCreate(BaseModel):
    """User creation schema."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None


class UserUpdate(BaseModel):
    """User update schema."""
    full_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None


class UserResponse(BaseModel):
    """User response schema."""
    id: str
    email: str
    username: str
    full_name: Optional[str]
    avatar_url: Optional[str]
    bio: Optional[str]
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ============= Authentication Schemas =============
class LoginRequest(BaseModel):
    """Login request schema."""
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Login response schema."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema."""
    refresh_token: str


class ChangePasswordRequest(BaseModel):
    """Change password request schema."""
    old_password: str
    new_password: str = Field(..., min_length=8)


# ============= Content Schemas =============
class ContentPieceCreate(BaseModel):
    """Create content piece schema."""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    script: str = Field(..., min_length=1)
    template_id: str
    voice_id: Optional[str] = None


class ContentPieceUpdate(BaseModel):
    """Update content piece schema."""
    title: Optional[str] = None
    description: Optional[str] = None
    script: Optional[str] = None
    voice_id: Optional[str] = None


class ContentPieceResponse(BaseModel):
    """Content piece response schema."""
    id: str
    creator_id: str
    title: str
    description: Optional[str]
    script: str
    template_id: str
    voice_id: Optional[str]
    status: ContentStatus
    duration: Optional[int]
    video_url: Optional[str]
    thumbnail_url: Optional[str]
    is_scheduled: bool
    scheduled_publish: Optional[datetime]
    published_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ContentScheduleRequest(BaseModel):
    """Schedule content request schema."""
    content_id: str
    scheduled_publish: datetime
    platforms: List[str] = []  # ['twitter', 'youtube', 'tiktok']


# ============= Analytics Schemas =============
class AnalyticsResponse(BaseModel):
    """Analytics response schema."""
    id: str
    user_id: str
    content_id: Optional[str]
    views: int
    likes: int
    shares: int
    comments: int
    engagement_rate: float
    ctr: float
    conversion_rate: float
    revenue: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    """Dashboard statistics schema."""
    total_views: int
    total_engagement: int
    total_revenue: float
    average_ctr: float
    top_content: List[ContentPieceResponse]
    recent_analytics: List[AnalyticsResponse]


# ============= Monetization Schemas =============
class MonetizationResponse(BaseModel):
    """Monetization response schema."""
    id: str
    user_id: str
    stripe_customer_id: Optional[str]
    subscription_plan: Optional[str]
    subscription_status: str
    total_earnings: float
    pending_payout: float
    paid_out: float
    payout_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SubscriptionRequest(BaseModel):
    """Subscription request schema."""
    plan: str  # 'starter', 'pro', 'enterprise'
    payment_method_id: str


# ============= Template Schemas =============
class TemplateResponse(BaseModel):
    """Template response schema."""
    id: str
    name: str
    description: Optional[str]
    thumbnail_url: Optional[str]
    category: str
    config: Optional[Dict[str, Any]]
    created_at: datetime

    class Config:
        from_attributes = True


# ============= Voice Schemas =============
class VoiceResponse(BaseModel):
    """Voice response schema."""
    id: str
    name: str
    language: str
    accent: Optional[str]
    gender: str
    description: Optional[str]
    provider: str
    created_at: datetime

    class Config:
        from_attributes = True


# ============= Error Schemas =============
class ErrorResponse(BaseModel):
    """Error response schema."""
    detail: str
    status_code: int
