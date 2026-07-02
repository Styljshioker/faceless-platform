"""Monetization API endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import Monetization
from app.schemas import MonetizationResponse, SubscriptionRequest

router = APIRouter()


@router.get("/", response_model=MonetizationResponse)
async def get_monetization_info(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user monetization information."""
    stmt = select(Monetization).where(Monetization.user_id == current_user["user_id"])
    result = await db.execute(stmt)
    monetization = result.scalars().first()
    
    if not monetization:
        # Create default monetization record
        monetization = Monetization(
            id=str(uuid.uuid4()),
            user_id=current_user["user_id"]
        )
        db.add(monetization)
        await db.commit()
        await db.refresh(monetization)
    
    return monetization


@router.post("/subscribe", response_model=MonetizationResponse)
async def subscribe(
    subscription_data: SubscriptionRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Subscribe to a plan."""
    stmt = select(Monetization).where(Monetization.user_id == current_user["user_id"])
    result = await db.execute(stmt)
    monetization = result.scalars().first()
    
    if not monetization:
        monetization = Monetization(
            id=str(uuid.uuid4()),
            user_id=current_user["user_id"]
        )
        db.add(monetization)
    
    # Update subscription
    monetization.subscription_plan = subscription_data.plan
    monetization.subscription_status = "active"
    
    await db.commit()
    await db.refresh(monetization)
    
    return monetization


@router.post("/payout-request")
async def request_payout(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Request payout of earnings."""
    stmt = select(Monetization).where(Monetization.user_id == current_user["user_id"])
    result = await db.execute(stmt)
    monetization = result.scalars().first()
    
    if not monetization:
        raise HTTPException(status_code=404, detail="Monetization info not found")
    
    if monetization.pending_payout <= 0:
        raise HTTPException(status_code=400, detail="No pending payout available")
    
    # Process payout
    monetization.paid_out += monetization.pending_payout
    monetization.pending_payout = 0
    monetization.payout_date = datetime.utcnow()
    
    await db.commit()
    await db.refresh(monetization)
    
    return {"message": "Payout processed", "monetization": monetization}


@router.get("/earnings")
async def get_earnings(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get earnings summary."""
    stmt = select(Monetization).where(Monetization.user_id == current_user["user_id"])
    result = await db.execute(stmt)
    monetization = result.scalars().first()
    
    if not monetization:
        return {
            "total_earnings": 0.0,
            "pending_payout": 0.0,
            "paid_out": 0.0
        }
    
    return {
        "total_earnings": monetization.total_earnings,
        "pending_payout": monetization.pending_payout,
        "paid_out": monetization.paid_out
    }


from datetime import datetime
