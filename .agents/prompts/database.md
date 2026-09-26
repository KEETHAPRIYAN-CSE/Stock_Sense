# Database Agent Prompt Template

When modifying or designing the database:
1. Review PostgreSQL requirements in `BUILD_STOCKSENSE.md` Section 14, 15, and 16.
2. Update SQLAlchemy models in `backend/app/models/`.
3. Generate and verify Alembic migrations in `backend/alembic/versions/`.
4. Ensure all foreign keys, unique constraints, and indices are defined.
5. Guarantee append-only behavior on `stock_ledger` and row locking on `stock_balances`.
