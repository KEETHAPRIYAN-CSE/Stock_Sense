# Codebase Audit — StockSense

## Objective
Audit the entire StockSense codebase against the `BUILD_STOCKSENSE_FINAL.md` master specification to establish the baseline and identify gaps.

## Current State
- **Backend**: FastAPI with SQLAlchemy, JWT auth, bcrypt password hashing, row-level locking inventory engine.
- **Database**: SQLite default for zero-config demo / PostgreSQL supported. Auto-table creation & seed migration configured on startup.
- **Frontend**: React + TypeScript + Vite, React Router, Axios client with JWT interceptor.
- **Test Suite**: 8/8 pytest tests passing (`test_auth.py`, `test_database_schema.py`, `test_health.py`, `test_inventory_invariants.py`, `test_master_data.py`).
- **Frontend Build**: `npm run build` succeeds cleanly.

## Key Observations & Gap Analysis
1. **Stock Page**: Currently displays SKU, Name, Total Qty, and Status. Wireframe / Spec requires:
   - Columns: Product, SKU/Code, Per Unit Cost (or Category), On Hand, Reserved, Free to Use (`Free to Use = On Hand - Reserved`).
   - Location / Warehouse filtering & Product search.
   - CSV export & clean visual styling.
2. **Operations (Receipts, Deliveries, Transfers, Adjustments)**:
   - Functioning CRUD and validation logic in backend with row-level locks and ledger writing.
   - Kanban / List view switcher needed for Move History and Operations.
   - Print capability (clean printable view / modal / browser print) for receipts & deliveries.
3. **Move History**:
   - Move History is currently mapped to `/ledger`. Needs search by reference, contact/user, date filter, status/operation filter, and CSV export.
4. **Dashboard**:
   - Live KPIs present (products, low stock, pending receipts/deliveries, transfers, warehouses, movements).
   - Needs Late / Waiting status indicators for receipts/deliveries.
5. **UI & Styling**:
   - Enhance dark theme aesthetics, typography, status badges, and responsive tables.
6. **Task Files**:
   - Initialize task files in `.agents/tasks/` for clear milestone tracking.

## Status
COMPLETED
