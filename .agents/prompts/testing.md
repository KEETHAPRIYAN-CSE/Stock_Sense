# Testing Agent Prompt Template

When writing or executing tests:
1. Verify all acceptance criteria defined in the task and `BUILD_STOCKSENSE.md`.
2. Cover positive flows, edge cases, and failure modes.
3. Test all five core inventory invariants:
   - Receipts add stock accurately.
   - Deliveries deduct stock and prevent overselling.
   - Transfers conserve total quantity across locations.
   - Adjustments correctly overwrite system quantity with physical count.
   - Ledger strictly maintains `quantity_after = quantity_before + quantity_change`.
4. Run `pytest` with verbose output.
