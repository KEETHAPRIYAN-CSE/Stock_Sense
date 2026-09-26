# Backend Agent Prompt Template

When working on backend tasks for StockSense:
1. Review `BUILD_STOCKSENSE.md` and `.agents/rules/backend.md`.
2. Inspect existing models, schemas, repositories, and services before making changes.
3. Keep route controllers thin and put business logic inside services (`app/services/`).
4. Ensure all stock adjustments, transfers, deliveries, and receipts execute inside explicit database transactions with row-level locks.
5. Provide type hints, docstrings, and comprehensive error responses.
