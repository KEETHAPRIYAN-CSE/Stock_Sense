# StockSense Authentication & Password Reset Flow

## Authentication
1. **Registration:** Users provide full name, email, password, and role (`INVENTORY_MANAGER` or `WAREHOUSE_STAFF`). Passwords are encrypted using Argon2/bcrypt.
2. **Login:** Verifies email and password hash. Issues a signed JWT access token containing user ID, email, and role.
3. **Session Management:** Stored in browser local storage or secure cookies; injected into outgoing Axios requests via standard `Bearer` token header.

## Secure OTP Password Reset
1. **Request Reset:** User submits their email to `POST /api/auth/forgot-password`.
   - The API generates a cryptographically secure 6-digit numeric OTP.
   - The OTP is hashed (e.g. SHA-256 with salt) and saved in `password_reset_otps` with `expires_at = now() + 10 minutes` and `attempt_count = 0`.
   - In development/demo mode, the OTP is returned in the response or logged safely for quick testing.
2. **Reset Execution:** User submits email, plain OTP, and new password to `POST /api/auth/reset-password`.
   - The system checks if active OTP exists, not expired, and attempt count < 5.
   - If invalid, attempt count increments.
   - If valid, user password hash is updated, and the OTP is marked `used_at = now()`.
