# StockSense Database Design & Schema

## Database Engine
- **Engine:** PostgreSQL 18
- **ORM / Migrations:** SQLAlchemy 2.0 & Alembic

## Entity Relationship Overview
- `users`: Core authentication, password hashes, roles (`INVENTORY_MANAGER`, `WAREHOUSE_STAFF`).
- `password_reset_otps`: OTP hashes, expirations, attempt counts.
- `categories`: Product classification hierarchy.
- `uoms`: Units of measure (e.g. Piece, Kilogram, Box, Meter).
- `products`: Master catalog with unique `sku`, reorder levels, initial stock.
- `warehouses`: Top-level storage facilities with unique `code`.
- `locations`: Specific storage racks, bays, or aisles within a warehouse (`UNIQUE(warehouse_id, code)`).
- `suppliers`: Vendors delivering goods.
- `customers`: Clients receiving goods.
- `stock_balances`: Real-time quantity of a product at a specific location (`UNIQUE(product_id, location_id)`).
- `stock_ledger`: Immutable append-only audit trail of every stock modification.
- `receipts` & `receipt_items`: Inbound inventory documents.
- `deliveries` & `delivery_items`: Outbound inventory documents.
- `transfers` & `transfer_items`: Inter-location movement documents.
- `adjustments` & `adjustment_items`: Discrepancy reconciliation documents.
- `reorder_rules`: Threshold definitions for automated replenishment warnings.

## Concurrency & Row Locking
All stock balance modifications lock the corresponding `stock_balances` row using `SELECT ... FOR UPDATE` before applying math, guaranteeing linearizable inventory balances under concurrent requests.
