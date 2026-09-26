from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import (
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    GoogleLoginRequest,
    ResetPasswordRequest,
    ResetPasswordResponse,
    Token,
    UserCreate,
    UserLogin,
    UserOut,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register a new user and return an access token."""
    auth_service = AuthService(db)
    user, access_token = auth_service.register(user_in)
    return Token(access_token=access_token, token_type="bearer", user=UserOut.model_validate(user))


@router.post("/login", response_model=Token)
def login(creds: UserLogin, db: Session = Depends(get_db)):
    """Authenticate a user using email and password, returning a JWT access token."""
    auth_service = AuthService(db)
    user, access_token = auth_service.authenticate(creds)
    return Token(access_token=access_token, token_type="bearer", user=UserOut.model_validate(user))


@router.post("/google", response_model=Token)
def login_google(req: GoogleLoginRequest, db: Session = Depends(get_db)):
    """Authenticate or register user via Google SSO."""
    auth_service = AuthService(db)
    user, access_token = auth_service.authenticate_google(req)
    return Token(access_token=access_token, token_type="bearer", user=UserOut.model_validate(user))



@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    """Stateless JWT logout endpoint."""
    return {"message": "Successfully logged out."}


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    """Retrieve profile of currently authenticated user."""
    return UserOut.model_validate(current_user)


@router.post("/forgot-password", response_model=ForgotPasswordResponse)
def forgot_password(req: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """Request a 6-digit password reset OTP."""
    auth_service = AuthService(db)
    msg, dev_otp = auth_service.request_password_reset(req.email)
    return ForgotPasswordResponse(message=msg, dev_otp=dev_otp)


@router.post("/reset-password", response_model=ResetPasswordResponse)
def reset_password(req: ResetPasswordRequest, db: Session = Depends(get_db)):
    """Reset password using 6-digit OTP."""
    auth_service = AuthService(db)
    auth_service.reset_password(req.email, req.otp, req.new_password)
    return ResetPasswordResponse(message="Password reset successfully. You can now log in.")
