from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User, PasswordResetOTP


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email.lower().strip()).first()

    def create(self, full_name: str, email: str, password_hash: str, role: str) -> User:
        user = User(
            full_name=full_name,
            email=email.lower().strip(),
            password_hash=password_hash,
            role=role,
            is_active=True,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_last_login(self, user: User) -> None:
        user.last_login_at = datetime.now(timezone.utc)
        self.db.commit()

    def update_password(self, user: User, password_hash: str) -> None:
        user.password_hash = password_hash
        user.updated_at = datetime.now(timezone.utc)
        self.db.commit()

    # OTP methods
    def create_otp(self, user_id: int, otp_hash: str, expires_at: datetime) -> PasswordResetOTP:
        otp_entry = PasswordResetOTP(
            user_id=user_id,
            otp_hash=otp_hash,
            expires_at=expires_at,
            attempt_count=0,
        )
        self.db.add(otp_entry)
        self.db.commit()
        self.db.refresh(otp_entry)
        return otp_entry

    def get_latest_otp(self, user_id: int) -> Optional[PasswordResetOTP]:
        return (
            self.db.query(PasswordResetOTP)
            .filter(
                PasswordResetOTP.user_id == user_id,
                PasswordResetOTP.used_at.is_(None),
            )
            .order_by(PasswordResetOTP.created_at.desc())
            .first()
        )

    def increment_otp_attempt(self, otp_entry: PasswordResetOTP) -> None:
        otp_entry.attempt_count += 1
        self.db.commit()

    def mark_otp_used(self, otp_entry: PasswordResetOTP) -> None:
        otp_entry.used_at = datetime.now(timezone.utc)
        self.db.commit()
