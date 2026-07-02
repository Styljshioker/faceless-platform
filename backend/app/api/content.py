"""Content creation API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import ContentPiece, ContentStatus
from app.schemas import (
    ContentPieceCreate, ContentPieceUpdate, ContentPieceResponse,
    ContentScheduleRequest
)

router = APIRouter()


@router.post("/", response_model=ContentPieceResponse)
async def create_content(
    content_data: ContentPieceCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new content piece."""
    content = ContentPiece(
        id=str(uuid.uuid4()),
        creator_id=current_user["user_id"],
        title=content_data.title,
        description=content_data.description,
        script=content_data.script,
        template_id=content_data.template_id,
        voice_id=content_data.voice_id,
        status=ContentStatus.DRAFT
    )
    db.add(content)
    await db.commit()
    await db.refresh(content)
    return content


@router.get("/", response_model=list[ContentPieceResponse])
async def list_content(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 10
):
    """List user's content pieces."""
    stmt = select(ContentPiece).where(
        ContentPiece.creator_id == current_user["user_id"]
    ).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/{content_id}", response_model=ContentPieceResponse)
async def get_content(
    content_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific content piece."""
    stmt = select(ContentPiece).where(ContentPiece.id == content_id)
    result = await db.execute(stmt)
    content = result.scalars().first()
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    if content.creator_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return content


@router.patch("/{content_id}", response_model=ContentPieceResponse)
async def update_content(
    content_id: str,
    content_data: ContentPieceUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a content piece."""
    stmt = select(ContentPiece).where(ContentPiece.id == content_id)
    result = await db.execute(stmt)
    content = result.scalars().first()
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    if content.creator_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Update fields
    if content_data.title:
        content.title = content_data.title
    if content_data.description is not None:
        content.description = content_data.description
    if content_data.script:
        content.script = content_data.script
    if content_data.voice_id:
        content.voice_id = content_data.voice_id
    
    await db.commit()
    await db.refresh(content)
    return content


@router.delete("/{content_id}")
async def delete_content(
    content_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a content piece."""
    stmt = select(ContentPiece).where(ContentPiece.id == content_id)
    result = await db.execute(stmt)
    content = result.scalars().first()
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    if content.creator_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    await db.delete(content)
    await db.commit()
    
    return {"message": "Content deleted successfully"}


@router.post("/{content_id}/schedule")
async def schedule_content(
    content_id: str,
    schedule_data: ContentScheduleRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Schedule content for publishing."""
    stmt = select(ContentPiece).where(ContentPiece.id == content_id)
    result = await db.execute(stmt)
    content = result.scalars().first()
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    if content.creator_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    content.is_scheduled = True
    content.scheduled_publish = schedule_data.scheduled_publish
    content.status = ContentStatus.PROCESSING
    
    await db.commit()
    await db.refresh(content)
    
    return {"message": "Content scheduled successfully", "content": content}


@router.post("/{content_id}/publish")
async def publish_content(
    content_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Publish a content piece."""
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
    
    return {"message": "Content published successfully", "content": content}
