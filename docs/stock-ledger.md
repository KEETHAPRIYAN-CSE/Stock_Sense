# StockSense Stock Movement Ledger

## Principles of the Ledger
The Stock Movement Ledger is the single source of truth for all historical inventory movements.

1. **Append-Only:** Ledger records are never edited or deleted. If an error occurs, a compensating transaction (e.g. adjustment) is created.
2. **Mathematical Invariant:** For every record:
   $$\text{quantity\_after} = \text{quantity\_before} + \text{quantity\_change}$$
3. **Traceability:** Every ledger record contains:
   - `product_id`: Which item moved.
   - `warehouse_id` & `location_id`: Where the movement took place.
   - `operation_type`: `INITIAL`, `RECEIPT`, `DELIVERY`, `TRANSFER_OUT`, `TRANSFER_IN`, or `ADJUSTMENT`.
   - `reference_type` & `reference_id`: Originating document (e.g. Receipt #REC-2026-001).
   - `quantity_before`, `quantity_change`, `quantity_after`.
   - `created_by`: User responsible for the action.
   - `created_at`: Timestamp.
   - `notes`: Reason or supplemental data.
