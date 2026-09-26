# Security Rules

1. Hash all passwords using Argon2 or bcrypt.
2. Store only salted hashes of OTPs in the database, never raw OTPs.
3. Enforce OTP expiration (10 minutes) and maximum attempt limits (e.g. 5 attempts).
4. Verify authentication and user role permissions on the backend API layer.
5. Sanitize all user inputs via Pydantic; always use parameterized SQLAlchemy queries to eliminate SQL injection.
6. Configure strict CORS and never leak sensitive stack traces or database errors in production responses.
7. Never print passwords, tokens, or OTPs in server logs.
