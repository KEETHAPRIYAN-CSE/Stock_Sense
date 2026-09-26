# StockSense Hackathon Demo Script

## Demo Script (Step-by-Step for Judges)

### Step 1: Authentication & Role Landing
- Log in as Inventory Manager (`manager@stocksense.com` / `admin123`).
- Land on dark-themed dashboard showing key KPIs: Total Products, Low Stock Alerts, Pending Receipts, Pending Deliveries, Scheduled Transfers.

### Step 2: Inbound Receipt (Stock Increase)
- Navigate to **Operations > Receipts**.
- Open Receipt for Supplier "Apex Industrial Supplies" containing **100 kg Steel Rods** to "Main Store".
- Click **Validate**.
- Show stock balance updated instantly (+100 kg) and an immutable `RECEIPT` ledger entry created.

### Step 3: Internal Transfer (Location Movement)
- Navigate to **Operations > Internal Transfers**.
- Create transfer: 20 kg Steel Rods from "Main Store" to "Production Rack".
- Click **Validate**.
- Demonstrate that Main Store decreases by 20, Production Rack increases by 20, and enterprise-wide total stock is strictly unchanged.

### Step 4: Customer Delivery (Outbound Fulfillment)
- Navigate to **Operations > Delivery Orders**.
- Open Delivery for Customer "BuildCorp Ltd" for 20 kg Steel Rods.
- Progress through **Pick** -> **Pack** -> **Validate**.
- Demonstrate stock decreasing by 20 kg and a `DELIVERY` ledger entry recorded.

### Step 5: Inventory Physical Count Adjustment
- Navigate to **Operations > Inventory Adjustments**.
- Perform adjustment on damaged inventory (-3 kg).
- Click **Validate**.
- Show stock now reconciles exactly to counted quantity (e.g. 77 kg).

### Step 6: Immutable Stock Movement Ledger
- Navigate to **Move History / Stock Ledger**.
- Show the complete audit trail with all timestamps, before/after values, reference IDs, and user attribution.
- Highlight that every single number is backed by PostgreSQL transactions.
