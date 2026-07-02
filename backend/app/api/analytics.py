"""Analytics API endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta
import uuid

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import Analytics, ContentPiece
from app.schemas import AnalyticsResponse, DashboardStats, ContentPieceResponse

router = APIRouter()


@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard_stats(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get dashboard statistics."""
    # Get total stats
    stmt = select(
        func.sum(Analytics.views).label('total_views'),
        func.sum(Analytics.likes).label('total_likes'),
        func.sum(Analytics.shares).label('total_shares'),
        func.sum(Analytics.revenue).label('total_revenue'),
        func.avg(Analytics.ctr).label('avg_ctr')
    ).where(Analytics.user_id == current_user["user_id"])
    
    result = await db.execute(stmt)
    row = result.first()
    
    total_views = row.total_views or 0
    total_revenue = row.total_revenue or 0.0
    avg_ctr = row.avg_ctr or 0.0
    total_engagement = (row.total_likes or 0) + (row.total_shares or 0)
    
    # Get top content
    stmt = select(ContentPiece).where(
        ContentPiece.creator_id == current_user["user_id"]
    ).order_by(ContentPiece.created_at.desc()).limit(5)
    result = await db.execute(stmt)
    top_content = result.scalars().all()
    
    # Get recent analytics
    stmt = select(Analytics).where(
        Analytics.user_id == current_user["user_id"]
    ).order_by(Analytics.created_at.desc()).limit(10)
    result = await db.execute(stmt)
    recent_analytics = result.scalars().all()
    
    return {
        "total_views": total_views,
        "total_engagement": total_engagement,
        "total_revenue": total_revenue,
        "average_ctr": avg_ctr,
        "top_content": top_content,
        "recent_analytics": recent_analytics
    }


@router.get("/", response_model=list[AnalyticsResponse])
async def get_analytics(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    days: int = 30,
    skip: int = 0,
    limit: int = 100
):
    """Get user analytics."""
    date_from = datetime.utcnow() - timedelta(days=days)
    
    stmt = select(Analytics).where(
        (Analytics.user_id == current_user["user_id"]) &
        (Analytics.created_at >= date_from)
    ).order_by(Analytics.created_at.desc()).offset(skip).limit(limit)
    
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/content/{content_id}", response_model=AnalyticsResponse)
async def get_content_analytics(
    content_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get analytics for a specific content."""
    stmt = select(Analytics).where(
        (Analytics.content_id == content_id) &
        (Analytics.user_id == current_user["user_id"])
    )
    result = await db.execute(stmt)
    analytics = result.scalars().first()
    
    if not analytics:
        raise HTTPException(status_code=404, detail="Analytics not found")
    
    return analytics


@router.post("/content/{content_id}/update")
async def update_content_analytics(
    content_id: str,
    views: int = 0,
    likes: int = 0,
    shares: int = 0,
    comments: int = 0,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update analytics for content."""
    stmt = select(Analytics).where(
        (Analytics.content_id == content_id) &
        (Analytics.user_id == current_user["user_id"])
    )
    result = await db.execute(stmt)
    analytics = result.scalars().first()
    
    if not analytics:
        # Create new analytics
        analytics = Analytics(
            id=str(uuid.uuid4()),
            user_id=current_user["user_id"],
            content_id=content_id,
            views=views,
            likes=likes,
            shares=shares,
            comments=comments
        )
        db.add(analytics)
    else:
        # Update existing
        analytics.views += views
        analytics.likes += likes
        analytics.shares += shares
        analytics.comments += comments
        
        # Calculate engagement rate
        total_interactions = analytics.likes + analytics.shares + analytics.comments
        if analytics.views > 0:
            analytics.engagement_rate = (total_interactions / analytics.views) * 100
    
    await db.commit()
    await db.refresh(analytics)
    
    return analytics
