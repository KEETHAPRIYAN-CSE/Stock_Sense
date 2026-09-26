# StockSense API Specification

## Conventions
- **Base URL:** `/api`
- **Authentication:** Bearer JWT in `Authorization` header (`Bearer <token>`).
- **Standard Responses:** JSON format with ISO 8601 timestamps.
- **Error Format:** `{"detail": "Descriptive error message"}`.

## Endpoints

### Auth
- `POST /api/auth/register` - Create new user account.
- `POST /api/auth/login` - Authenticate and obtain JWT access token.
- `POST /api/auth/logout` - Invalidate session client-side.
- `GET  /api/auth/me` - Retrieve current user profile and role.
- `POST /api/auth/forgot-password` - Request password reset OTP.
- `POST /api/auth/reset-password` - Reset password using verified OTP.

### Master Data
- `GET, POST /api/products` & `GET, PUT, DELETE /api/products/{id}`
- `GET, POST /api/categories` & `PUT /api/categories/{id}`
- `GET, POST /api/uoms`
- `GET, POST /api/warehouses` & `PUT /api/warehouses/{id}`
- `GET, POST /api/locations` & `PUT /api/locations/{id}`
- `GET, POST /api/suppliers` & `PUT /api/suppliers/{id}`
- `GET, POST /api/customers` & `PUT /api/customers/{id}`

### Operations
- `GET, POST /api/receipts`, `GET /api/receipts/{id}`, `POST /api/receipts/{id}/validate`, `POST /api/receipts/{id}/cancel`
- `GET, POST /api/deliveries`, `GET /api/deliveries/{id}`, `POST /api/deliveries/{id}/pick`, `POST /api/deliveries/{id}/pack`, `POST /api/deliveries/{id}/validate`, `POST /api/deliveries/{id}/cancel`
- `GET, POST /api/transfers`, `GET /api/transfers/{id}`, `POST /api/transfers/{id}/validate`, `POST /api/transfers/{id}/cancel`
- `GET, POST /api/adjustments`, `GET /api/adjustments/{id}`, `POST /api/adjustments/{id}/validate`, `POST /api/adjustments/{id}/cancel`

### Stock & Ledger
- `GET /api/stock` - Aggregated stock levels across all locations.
- `GET /api/stock/{product_id}/locations` - Location-specific breakdown for a product.
- `GET /api/stock/ledger` - Paginated immutable stock movement audit ledger with filters.

### Dashboard
- `GET /api/dashboard/summary` - Key performance metrics (Total Products, Low Stock, Pending Receipts, Pending Deliveries, Scheduled Transfers).
- `GET /api/dashboard/operations` - Status distribution and document counts.
- `GET /api/dashboard/low-stock` - Products below reorder thresholds.
