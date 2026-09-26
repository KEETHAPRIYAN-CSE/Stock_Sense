# Testing Rules

1. Every P0 feature must be covered by automated tests.
2. Invariants must be asserted in pytest test suites:
   - Receipts increase stock and create valid ledger rows.
   - Deliveries decrease stock, cannot exceed available stock, and record ledger rows.
   - Transfers leave total stock unchanged across locations.
   - Adjustments reconcile system count to physical count accurately.
   - Ledger append-only invariant holds: `quantity_after == quantity_before + quantity_change`.
3. Test authentication edge cases: bad credentials, expired OTPs, re-using OTPs, unauthorized calls.
4. Run backend tests using `pytest` and frontend verification using TypeScript / build checks.
