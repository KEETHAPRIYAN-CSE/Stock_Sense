# Backend Development Rules

1. Use FastAPI and Python 3.12+ with strict typing and Pydantic schemas.
2. Maintain clean layer separation:
   - Routers (`app/api/`) only handle HTTP request/response validation and status codes.
   - Services (`app/services/`) execute core business logic, transactions, and inventory invariants.
   - Repositories (`app/repositories/`) manage database queries and locks.
3. Every stock-changing operation MUST execute inside a database transaction with proper row locking (`with_for_update`).
4. Centralize all stock modifications in `InventoryService` (`receive_stock`, `deliver_stock`, `transfer_stock`, `adjust_stock`).
5. Never duplicate stock math in API route handlers.
6. Use consistent error handling and standard HTTP status codes.
