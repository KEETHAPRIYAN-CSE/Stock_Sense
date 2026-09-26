# StockSense Security Specification

## Security Controls
1. **Password Storage:** Encrypted with modern algorithms (Argon2 / bcrypt) with salt.
2. **JWT Authentication:** Signed access tokens using HMAC-SHA256 with 24-hour expiration.
3. **Role-Based Access Control (RBAC):**
   - Endpoints require explicit roles (`INVENTORY_MANAGER`, `WAREHOUSE_STAFF`).
   - Server-side dependency checks verify token validity and role authorization on every protected route.
4. **Input Sanitization & Injection Prevention:**
   - Strict Pydantic models validate data types, string lengths, and ranges.
   - SQLAlchemy parameterized queries eliminate SQL injection vulnerabilities.
5. **CORS:** Configured for allowed development origins (`localhost:5173`, `localhost:3000`).
6. **No Secret Leakage:**
   - Error handlers catch exceptions and return sanitized messages (`{"detail": "..."}`).
   - Stack traces and database connection strings are never exposed in responses or public logs.
