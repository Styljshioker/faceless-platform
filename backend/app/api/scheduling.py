"""Scheduling API endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import ContentPiece, ContentStatus
from app.schemas import ContentPieceResponse

router = APIRouter()


@router.get("/scheduled", response_model=list[ContentPieceResponse])
async def get_scheduled_content(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get scheduled content."""
    stmt = select(ContentPiece).where(
        (ContentPiece.creator_id == current_user["user_id"]) &
        (ContentPiece.is_scheduled == True)
    ).order_by(ContentPiece.scheduled_publish)
    
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/pending", response_model=list[ContentPieceResponse])
async def get_pending_content(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get pending content ready to publish."""
    now = datetime.utcnow()
    stmt = select(ContentPiece).where(
        (ContentPiece.creator_id == current_user["user_id"]) &
        (ContentPiece.is_scheduled == True) &
        (ContentPiece.scheduled_publish <= now) &
        (ContentPiece.status != ContentStatus.PUBLISHED)
    ).order_by(ContentPiece.scheduled_publish)
    
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("/publish-now/{content_id}")
async def publish_scheduled_now(
    content_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Publish scheduled content immediately."""
    stmt = select(ContentPiece).where(ContentPiece.id == content_id)
    result = await db.execute(stmt)
    content = result.scalars().first()
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    if content.creator_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    content.status = ContentStatus.PUBLISHED
    content.published_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(content)
    
    return {"message": "Content published immediately", "content": content}
