import random
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import (
    create_access_token,
    get_password_hash,
    hash_otp,
    verify_otp_hash,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate, UserLogin


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)

    def register(self, user_in: UserCreate) -> Tuple[User, str]:
        existing = self.repo.get_by_email(user_in.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email address already exists.",
            )

        hashed_pw = get_password_hash(user_in.password)
        user = self.repo.create(
            full_name=user_in.full_name,
            email=user_in.email,
            password_hash=hashed_pw,
            role=user_in.role,
        )
        token = create_access_token(subject=user.id, role=user.role)
        return user, token

    def authenticate(self, creds: UserLogin) -> Tuple[User, str]:
        user = self.repo.get_by_email(creds.email)
        if not user or not verify_password(creds.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user account.",
            )

        self.repo.update_last_login(user)
        token = create_access_token(subject=user.id, role=user.role)
        return user, token

    def request_password_reset(self, email: str) -> Tuple[str, Optional[str]]:
        user = self.repo.get_by_email(email)
        # Even if user does not exist, return generic message to prevent account enumeration
        if not user:
            return "If your email is registered, you will receive an OTP shortly.", None

        # Generate a 6-digit numeric OTP
        raw_otp = f"{random.randint(100000, 999999)}"
        hashed = hash_otp(raw_otp)
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)

        self.repo.create_otp(user_id=user.id, otp_hash=hashed, expires_at=expires_at)

        # In development/testing return raw_otp for testing
        dev_otp = raw_otp if settings.ENVIRONMENT in ["development", "test"] else None
        return "If your email is registered, you will receive an OTP shortly.", dev_otp

    def reset_password(self, email: str, raw_otp: str, new_password: str) -> None:
        user = self.repo.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid request or expired OTP.",
            )

        otp_record = self.repo.get_latest_otp(user.id)
        if not otp_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid request or expired OTP.",
            )

        # Check maximum attempts (5)
        if otp_record.attempt_count >= 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Maximum verification attempts exceeded. Please request a new OTP.",
            )

        # Check expiration
        now = datetime.now(timezone.utc)
        record_expires = otp_record.expires_at
        if record_expires.tzinfo is None:
            record_expires = record_expires.replace(tzinfo=timezone.utc)

        if now > record_expires:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OTP has expired. Please request a new one.",
            )

        # Verify hash
        if not verify_otp_hash(raw_otp, otp_record.otp_hash):
            self.repo.increment_otp_attempt(otp_record)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid OTP.",
            )

        # Mark OTP used and update password
        self.repo.mark_otp_used(otp_record)
        new_hash = get_password_hash(new_password)
        self.repo.update_password(user, new_hash)
