from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.schemas.auth import AuthResponse, LoginRequest, RegisterRequest
from app.services.auth_service import AuthError, login, register

router = APIRouter()


@router.post("/register", response_model=AuthResponse)
async def register_user(body: RegisterRequest, db: Session = Depends(get_db)):
    try:
        if len(body.password) < 8:
            raise AuthError("Password must be at least 8 characters")
        result = register(db, body.name, body.email, body.password)
        return result
    except AuthError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=AuthResponse)
async def login_user(
    body: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        auth_result, access_token, refresh_token = login(db, body.email, body.password)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=settings.access_token_expire_minutes * 60,
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
        )
        return auth_result
    except AuthError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out"}
