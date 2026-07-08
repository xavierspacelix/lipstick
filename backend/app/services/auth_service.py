from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.schemas.auth import AuthResponse


class AuthError(Exception):
    pass


def register(db: Session, name: str, email: str, password: str) -> AuthResponse:
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise AuthError("Email already registered")

    user = User(
        name=name,
        email=email,
        password_hash=hash_password(password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return AuthResponse(user_id=user.id, name=user.name, email=user.email)


def login(db: Session, email: str, password: str) -> tuple[AuthResponse, str, str]:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise AuthError("Invalid email or password")

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return (
        AuthResponse(user_id=user.id, name=user.name, email=user.email),
        access_token,
        refresh_token,
    )
