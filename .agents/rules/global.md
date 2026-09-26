# Global Development Rules

1. Read project documentation before making changes (`BUILD_STOCKSENSE.md`, `WORKFLOW.md`, `docs/*`).
2. Preserve architecture and clean separation of concerns.
3. Test every change: no code is considered done without verification.
4. Never commit secrets, credentials, or actual `.env` files.
5. Never fake backend data or return hardcoded mock responses for P0 features.
6. Inventory transactional integrity is strictly paramount: every stock change must produce a ledger entry and update stock balance within a transaction.
7. Maintain clean documentation and update task files after each verified step.
