from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user, hash_password, verify_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.profile import (
    ChangePasswordRequest,
    ProfileResponse,
    ProfileStats,
    UpdateProfileRequest,
)

router = APIRouter()


@router.get("/profile", response_model=ProfileResponse)
async def get_profile(
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return ProfileResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        total_analyses=user.total_analyses,
    )


@router.patch("/profile", response_model=ProfileResponse)
async def update_profile(
    body: UpdateProfileRequest,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = body.name
    db.commit()
    db.refresh(user)

    return ProfileResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        total_analyses=user.total_analyses,
    )


@router.patch("/profile/password")
async def change_password(
    body: ChangePasswordRequest,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(body.current_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    user.password_hash = hash_password(body.new_password)
    db.commit()

    return {"message": "Password updated"}


@router.get("/profile/stats", response_model=ProfileStats)
async def get_profile_stats(
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return ProfileStats(total_analyses=user.total_analyses)
