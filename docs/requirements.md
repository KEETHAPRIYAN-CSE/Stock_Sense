# StockSense Requirements & Scope

## Users & Personas
- **Inventory Manager:** Oversees warehouse operations, sets reorder levels, manages suppliers, customers, and validates high-level transactions.
- **Warehouse Staff:** Performs stock receiving, picks and packs deliveries, executes internal rack/bay transfers, and records physical count reconciliations.

## Scope Breakdown

### P0 (Core MVP - Mandatory)
1. **Authentication:** User registration, login, logout, password reset with secure time-limited OTP.
2. **Master Data:** Products (SKU, Category, UOM, Reorder Level), Warehouses, Locations, Suppliers, Customers.
3. **Core Operations:**
   - **Receipts:** Incoming stock from suppliers into a designated warehouse location.
   - **Deliveries:** Stock dispatches to customers with Pick, Pack, and Validate workflows.
   - **Transfers:** Moving items between locations/warehouses preserving company-wide total stock.
   - **Adjustments:** Physical count reconciliation recording damaged/found items.
4. **Stock Balances & Immutable Ledger:** Atomic transaction-locked updates with complete movement history.
5. **Dashboard:** Real-time KPI cards (Total Products, Low Stock, Pending Receipts, Pending Deliveries, Scheduled Transfers) with filtering.
6. **Dark Wireframe-Aligned UI:** Responsive, high-contrast, coral accent UI with Loading/Empty/Error states.

### P1 (Extended Features)
- Reorder threshold alerts and notification banners.
- Batch export of stock ledger to CSV/Excel.
- Detailed audit logs for master data edits.

### P2 (Future Additions)
- Barcode/QR scanning integration.
- Automated purchase order generation.
