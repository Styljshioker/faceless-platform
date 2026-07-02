"""Authentication API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta
import uuid

from app.core.database import get_db
from app.core.security import (
    hash_password, verify_password, create_access_token, get_current_user
)
from app.core.config import settings
from app.models import User
from app.schemas import (
    UserCreate, LoginRequest, LoginResponse, UserResponse,
    ChangePasswordRequest
)

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user."""
    # Check if user exists
    stmt = select(User).where(
        (User.email == user_data.email) | (User.username == user_data.username)
    )
    existing = await db.execute(stmt)
    if existing.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email or username already registered"
        )
    
    # Create new user
    user = User(
        id=str(uuid.uuid4()),
        email=user_data.email,
        username=user_data.username,
        hashed_password=hash_password(user_data.password),
        full_name=user_data.full_name
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/login", response_model=LoginResponse)
async def login(credentials: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Login user and return access token."""
    stmt = select(User).where(User.email == credentials.email)
    result = await db.execute(stmt)
    user = result.scalars().first()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    access_token = create_access_token(data={"sub": user.id})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.post("/change-password")
async def change_password(
    request: ChangePasswordRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Change user password."""
    stmt = select(User).where(User.id == current_user["user_id"])
    result = await db.execute(stmt)
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not verify_password(request.old_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )
    
    user.hashed_password = hash_password(request.new_password)
    await db.commit()
    
    return {"message": "Password changed successfully"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user information."""
    stmt = select(User).where(User.id == current_user["user_id"])
    result = await db.execute(stmt)
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
