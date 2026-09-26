# StockSense Inventory Engine & Business Invariants

## Core Operations

### 1. Inbound Receipts
- **Trigger:** `POST /api/receipts/{id}/validate`
- **Execution:**
  1. Lock target `stock_balances(product_id, destination_location_id)`.
  2. Increase balance: `new_qty = current_qty + receipt_qty`.
  3. Append to `stock_ledger` with `operation_type = RECEIPT`.
  4. Mark receipt status as `DONE`.
- **Invariant:** `after = before + received`.

### 2. Outbound Deliveries
- **Trigger:** `POST /api/deliveries/{id}/validate`
- **Execution:**
  1. Lock source `stock_balances(product_id, source_location_id)`.
  2. Verify available stock: `current_qty >= delivery_qty`. If not, abort with HTTP 400.
  3. Decrease balance: `new_qty = current_qty - delivery_qty`.
  4. Append to `stock_ledger` with `operation_type = DELIVERY`.
  5. Mark delivery status as `DONE`.
- **Invariant:** `after = before - delivered` and `delivered <= available`.

### 3. Internal Transfers
- **Trigger:** `POST /api/transfers/{id}/validate`
- **Execution:**
  1. Lock source and destination balances in consistent order to prevent deadlocks.
  2. Check source: `source_qty >= transfer_qty`.
  3. Decrease source: `source_after = source_before - transfer_qty`.
  4. Increase destination: `dest_after = dest_before + transfer_qty`.
  5. Append two ledger entries: `TRANSFER_OUT` and `TRANSFER_IN`.
  6. Mark transfer status as `DONE`.
- **Invariant:** Total enterprise quantity remains unchanged: `source_change + dest_change = 0`.

### 4. Stock Adjustments
- **Trigger:** `POST /api/adjustments/{id}/validate`
- **Execution:**
  1. Lock target balance.
  2. Calculate `difference = counted_quantity - system_quantity`.
  3. Set `quantity = counted_quantity`.
  4. Append ledger row with `operation_type = ADJUSTMENT`, `quantity_change = difference`.
  5. Mark adjustment status as `DONE`.
- **Invariant:** `new_quantity = counted_quantity` and `difference = counted - system`.
