# Database Development Rules

1. PostgreSQL is the authoritative system of record.
2. All schema changes must be version-controlled via Alembic migrations.
3. Preserve foreign-key integrity, explicit unique constraints, and check constraints.
4. Stock changes require database row locks (`SELECT ... FOR UPDATE`) on the relevant `stock_balances` rows.
5. Invariant enforcement:
   - Quantities must not drop below zero on deliveries/transfers.
   - `stock_ledger` entries must be append-only with formula: `quantity_after = quantity_before + quantity_change`.
6. Indexes must be created on heavily queried fields (SKU, product_id, location_id, reference_type, status, created_at).
