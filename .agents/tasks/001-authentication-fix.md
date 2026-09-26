# Task: Authentication & Authorization Verification

## Objective
Verify that the end-to-end authentication flow works seamlessly with persistent database records and RBAC guards:
1. User Registration (`/api/auth/register`) creates a real DB user with hashed password and generates JWT.
2. User Login (`/api/auth/login`) accepts the new credentials and issues valid token.
3. `/api/auth/me` retrieves authenticated user profile and role.
4. Forgot Password (`/api/auth/forgot-password`) creates a hashed OTP in `password_reset_otps` with expiration.
5. Password Reset (`/api/auth/reset-password`) validates OTP hash, resets password, and allows login with the new password.
6. Old password is confirmed rejected.

## Current State
- `backend/app/api/v1/auth.py` and `backend/app/services/auth_service.py` implemented.
- `backend/app/core/init_db.py` ensures tables and seed demo credentials exist on boot.
- Pytest suite `tests/test_auth.py` verified and passing 100%.

## Acceptance Criteria
- [x] Persistent DB storage for users and OTPs
- [x] Passwords salted and hashed with bcrypt
- [x] JWT token generated with expiration
- [x] OTP attempt tracking and invalidation
- [x] Automated integration tests passing

## Status
VERIFIED & COMPLETED
