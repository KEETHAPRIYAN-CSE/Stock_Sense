# StockSense --- Autonomous Full-Stack Build Specification #

## Purpose

You are the primary coding agent for the **StockSense Inventory
Management System**.

Your job is to build the complete working application from this
specification.

Do not merely describe code. **Create the directories, create the files,
write the implementation, create the database schema and migrations, run
the application checks, run tests, fix errors, and leave the repository
in a runnable state.**

The application must be suitable for a time-constrained hackathon, so
prioritize:

1.  Correct inventory transactions
2.  Data integrity
3.  Working authentication
4.  Complete core CRUD and operations
5.  Clear dashboard
6.  Clean, responsive UI
7.  Automated tests
8.  Easy local setup
9.  Simple architecture that can be explained during judging

Do not introduce unnecessary technologies such as microservices, Kafka,
Kubernetes, blockchain, RAG, or AI features unless explicitly requested
later.

------------------------------------------------------------------------

# 1. NON-NEGOTIABLE AGENT RULES

## 1.1 Build, don't just explain

When executing this document:

-   Create missing folders.
-   Create missing files.
-   Write complete code.
-   Never leave TODO placeholders in P0 functionality.
-   Never create fake API responses when the real database/API can be
    implemented.
-   Never hard-code inventory values into the UI.
-   Never silently skip an acceptance criterion.

## 1.2 Inspect before modifying

Before changing an existing repository:

1.  Inspect the current directory.
2.  Inspect existing files.
3.  Detect the existing package managers and frameworks.
4.  Preserve useful existing work.
5.  Avoid overwriting working code unnecessarily.
6.  Reuse existing configuration when compatible.

## 1.3 Small verified steps

Work in atomic phases.

After each major phase:

1.  Run the relevant checks.
2.  Fix errors.
3.  Re-run the checks.
4.  Only then continue.

If a phase fails, do not continue building on broken code.

## 1.4 Human approval gates

Ask for human approval before:

-   destructive database deletion,
-   production database changes,
-   deleting major existing features,
-   changing authentication/security architecture,
-   replacing the selected framework,
-   adding expensive/external services,
-   deploying to production.

For local development, creating a new database or running migrations is
allowed when clearly documented and non-destructive.

## 1.5 Secrets

Never:

-   commit `.env`,
-   hard-code passwords,
-   hard-code JWT secrets,
-   hard-code API keys,
-   print secrets in logs.

Create `.env.example` files instead.

------------------------------------------------------------------------

# 2. PROJECT NAME

**StockSense**

Inventory Management System.

Target users:

-   Inventory Managers
-   Warehouse Staff

Core objective:

Replace manual registers, Excel sheets, and scattered inventory tracking
with a centralized inventory system that maintains current stock and a
complete stock movement ledger.

------------------------------------------------------------------------

# 3. TECHNOLOGY STACK

Use the following stack unless the repository already contains a
compatible implementation that should be preserved.

## Backend

-   Python 3.x
-   FastAPI
-   SQLAlchemy 2.x
-   Alembic
-   PostgreSQL
-   Pydantic
-   JWT authentication
-   bcrypt/Argon2-compatible password hashing

## Frontend

-   React
-   TypeScript
-   Vite
-   React Router
-   Axios or fetch
-   A clean component-based UI

## Development

-   Git
-   `.env`
-   pytest
-   ESLint/TypeScript checks where configured

------------------------------------------------------------------------

# 4. REQUIRED PROJECT STRUCTURE

Create this structure:

``` text
StockSense/
│
├── WORKFLOW.md
├── BUILD_STOCKSENSE.md
├── README.md
├── .gitignore
├── .env.example
├── docker-compose.yml
│
├── .agents/
│   ├── rules/
│   │   ├── global.md
│   │   ├── backend.md
│   │   ├── frontend.md
│   │   ├── database.md
│   │   ├── security.md
│   │   ├── testing.md
│   │   └── git.md
│   ├── prompts/
│   │   ├── backend.md
│   │   ├── frontend.md
│   │   ├── database.md
│   │   ├── testing.md
│   │   └── code-review.md
│   ├── tasks/
│   └── handoffs/
│
├── docs/
│   ├── problem.md
│   ├── requirements.md
│   ├── architecture.md
│   ├── database.md
│   ├── api.md
│   ├── authentication.md
│   ├── inventory-engine.md
│   ├── stock-ledger.md
│   ├── security.md
│   ├── testing.md
│   ├── deployment.md
│   └── demo-script.md
│
├── backend/
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── .env.example
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── repositories/
│   │   ├── services/
│   │   ├── api/
│   │   └── utils/
│   └── tests/
│
├── frontend/
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── index.html
│   └── src/
│
├── scripts/
│   ├── create_database.sql
│   ├── seed_demo_data.sql
│   ├── seed_database.py
│   ├── reset_database.py
│   └── health_check.py
│
└── tests/
    └── integration/
```

------------------------------------------------------------------------

# 5. FUNCTIONAL REQUIREMENTS

## 5.1 Authentication

Implement:

-   Sign up
-   Login
-   Logout
-   Current-user endpoint
-   Forgot password
-   OTP-based password reset
-   Password hashing
-   Protected API routes

After successful login, redirect to Inventory Dashboard.

OTP requirements:

-   Store a hash of the OTP, not plaintext.
-   Expire OTPs.
-   Limit attempts.
-   Mark used OTPs.
-   Do not reveal whether an email exists through unsafe error messages.
-   Never log OTP values.

------------------------------------------------------------------------

# 6. DASHBOARD

Dashboard must display:

-   Total Products in Stock
-   Low Stock / Out of Stock
-   Pending Receipts
-   Pending Deliveries
-   Internal Transfers Scheduled

Provide dynamic filtering for:

-   Document type:
    -   Receipts
    -   Delivery
    -   Internal
    -   Adjustments
-   Status:
    -   Draft
    -   Waiting
    -   Ready
    -   Done
    -   Canceled
-   Warehouse/location
-   Product category

Dashboard data must come from the backend/database.

Do not hard-code KPI values.

------------------------------------------------------------------------

# 7. NAVIGATION

Create:

``` text
Dashboard

Products

Operations
├── Receipts
├── Delivery Orders
├── Internal Transfers
├── Inventory Adjustments
└── Move History / Stock Ledger

Settings
└── Warehouses / Locations

Profile
├── My Profile
└── Logout
```

------------------------------------------------------------------------

# 8. PRODUCT MANAGEMENT

Users must be able to:

-   Create products
-   View products
-   Update products
-   Search products
-   Filter products
-   View stock by location
-   Configure categories
-   Configure reorder levels

Product fields:

``` text
id
name
sku/code
category
unit of measure
initial stock
reorder level
active
created_at
updated_at
```

SKU must be unique.

------------------------------------------------------------------------

# 9. RECEIPTS

A receipt represents incoming stock.

Users can:

1.  Create receipt.
2.  Select supplier.
3.  Add products and quantities.
4.  Save receipt.
5.  Move through operational status.
6.  Validate receipt.
7.  Increase stock automatically.
8.  Create stock ledger entries.

Example:

``` text
Before: 100 Steel Rods
Receipt: +50
After: 150 Steel Rods
```

The receipt validation and stock update must occur in one database
transaction.

------------------------------------------------------------------------

# 10. DELIVERY ORDERS

A delivery represents stock leaving a warehouse for a customer.

Workflow:

``` text
Draft
  ↓
Waiting
  ↓
Ready
  ↓
Pick
  ↓
Pack
  ↓
Validate
  ↓
Done
```

On final validation:

``` text
new_stock = old_stock - delivered_quantity
```

Never allow delivery quantity greater than available stock.

Create corresponding ledger entries.

------------------------------------------------------------------------

# 11. INTERNAL TRANSFERS

Support:

``` text
Main Warehouse → Production Floor
Rack A → Rack B
Warehouse 1 → Warehouse 2
```

A transfer must:

1.  Validate available source stock.
2.  Decrease source location.
3.  Increase destination location.
4.  Create source ledger entry.
5.  Create destination ledger entry.
6.  Commit everything atomically.

Example:

``` text
Main Store: 100
Transfer: 20
Main Store: 80
Production Rack: +20
Total company stock: unchanged
```

------------------------------------------------------------------------

# 12. STOCK ADJUSTMENTS

Stock adjustments reconcile system quantity against physical count.

Fields:

``` text
product
location
system_quantity
counted_quantity
difference
reason
```

Formula:

``` text
difference = counted_quantity - system_quantity
new_quantity = counted_quantity
```

Example:

``` text
System: 50
Physical: 47
Difference: -3
New stock: 47
```

Create a ledger entry.

------------------------------------------------------------------------

# 13. STOCK LEDGER

The stock ledger is a core source of truth for inventory history.

Ledger fields:

``` text
id
product_id
warehouse_id
location_id
operation_type
reference_type
reference_id
quantity_before
quantity_change
quantity_after
created_by
created_at
notes
```

Operation types:

``` text
INITIAL
RECEIPT
DELIVERY
TRANSFER_OUT
TRANSFER_IN
ADJUSTMENT
```

Ledger must be append-only.

Do not edit historical ledger rows to correct mistakes.

Corrections must be represented by a new compensating transaction.

Invariant:

``` text
quantity_after = quantity_before + quantity_change
```

------------------------------------------------------------------------

# 14. DATABASE SCHEMA

Use PostgreSQL.

Create these tables.

## users

``` text
id
full_name
email UNIQUE
password_hash
role
is_active
created_at
updated_at
last_login_at
```

## password_reset_otps

``` text
id
user_id FK users
otp_hash
expires_at
attempt_count
used_at
created_at
```

## categories

``` text
id
name
description
is_active
created_at
updated_at
```

## uoms

``` text
id
name
code
is_active
created_at
```

## products

``` text
id
name
sku UNIQUE
category_id FK categories
uom_id FK uoms
initial_stock
reorder_level
is_active
created_at
updated_at
```

## warehouses

``` text
id
name
code UNIQUE
address
is_active
created_at
updated_at
```

## locations

``` text
id
warehouse_id FK warehouses
name
code
location_type
is_active
created_at
updated_at

UNIQUE(warehouse_id, code)
```

## suppliers

``` text
id
name
contact_name
email
phone
is_active
created_at
updated_at
```

## customers

``` text
id
name
email
phone
address
is_active
created_at
updated_at
```

## stock_balances

``` text
id
product_id FK products
location_id FK locations
quantity
updated_at

UNIQUE(product_id, location_id)
```

## stock_ledger

``` text
id
product_id FK products
warehouse_id FK warehouses
location_id FK locations
operation_type
reference_type
reference_id
quantity_before
quantity_change
quantity_after
created_by FK users
created_at
notes
```

## receipts

``` text
id
receipt_number UNIQUE
supplier_id FK suppliers
warehouse_id FK warehouses
destination_location_id FK locations
status
scheduled_at
created_by FK users
validated_by FK users
created_at
updated_at
validated_at
```

## receipt_items

``` text
id
receipt_id FK receipts
product_id FK products
quantity
uom_id FK uoms
created_at
```

## deliveries

``` text
id
delivery_number UNIQUE
customer_id FK customers
warehouse_id FK warehouses
source_location_id FK locations
status
scheduled_at
created_by FK users
validated_by FK users
created_at
updated_at
validated_at
```

## delivery_items

``` text
id
delivery_id FK deliveries
product_id FK products
quantity
uom_id FK uoms
picked_quantity
packed_quantity
created_at
```

## transfers

``` text
id
transfer_number UNIQUE
warehouse_id FK warehouses
source_location_id FK locations
destination_location_id FK locations
status
scheduled_at
created_by FK users
validated_by FK users
created_at
updated_at
validated_at
```

## transfer_items

``` text
id
transfer_id FK transfers
product_id FK products
quantity
uom_id FK uoms
created_at
```

## adjustments

``` text
id
adjustment_number UNIQUE
warehouse_id FK warehouses
location_id FK locations
status
reason
created_by FK users
validated_by FK users
created_at
updated_at
validated_at
```

## adjustment_items

``` text
id
adjustment_id FK adjustments
product_id FK products
system_quantity
counted_quantity
difference
created_at
```

## reorder_rules

``` text
id
product_id FK products
location_id FK locations
minimum_quantity
maximum_quantity
is_active
created_at
updated_at
```

------------------------------------------------------------------------

# 15. DATABASE CONSTRAINTS

Implement appropriate:

-   Primary keys
-   Foreign keys
-   Unique constraints
-   NOT NULL constraints
-   Check constraints where useful
-   Indexes

Required uniqueness:

``` text
users.email
products.sku
warehouses.code
locations(warehouse_id, code)
receipts.receipt_number
deliveries.delivery_number
transfers.transfer_number
adjustments.adjustment_number
```

Recommended indexes:

``` text
stock_ledger(product_id)
stock_ledger(location_id)
stock_ledger(created_at)
stock_ledger(reference_type, reference_id)
stock_balances(product_id, location_id)
products(category_id)
products(sku)
receipts(status)
deliveries(status)
transfers(status)
adjustments(status)
```

Quantities must not become negative where business rules prohibit them.

------------------------------------------------------------------------

# 16. DATABASE TRANSACTION RULE

Every stock-changing operation must use a database transaction.

For receipt:

``` text
BEGIN
→ lock relevant stock balance
→ calculate before
→ update stock balance
→ insert ledger
→ mark receipt DONE
→ COMMIT
```

For delivery:

``` text
BEGIN
→ lock stock balance
→ verify available quantity
→ decrease stock
→ insert ledger
→ mark delivery DONE
→ COMMIT
```

For transfer:

``` text
BEGIN
→ lock source balance
→ verify source quantity
→ decrease source
→ increase destination
→ insert TRANSFER_OUT ledger
→ insert TRANSFER_IN ledger
→ mark transfer DONE
→ COMMIT
```

For adjustment:

``` text
BEGIN
→ lock balance
→ read system quantity
→ calculate difference
→ set counted quantity
→ insert ledger
→ mark adjustment DONE
→ COMMIT
```

Rollback the complete transaction if any operation fails.

------------------------------------------------------------------------

# 17. INVENTORY SERVICE

Create a centralized inventory service.

Required functions:

``` python
receive_stock()
deliver_stock()
transfer_stock()
adjust_stock()
get_stock()
get_stock_by_location()
get_ledger()
```

Do not duplicate stock-changing logic inside individual route handlers.

Routes should call services.

Services should perform business logic.

Repositories should handle database access where appropriate.

------------------------------------------------------------------------

# 18. API

Implement these endpoints.

## Authentication

``` text
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout
GET  /api/auth/me
POST /api/auth/forgot-password
POST /api/auth/reset-password
```

## Products

``` text
GET    /api/products
POST   /api/products
GET    /api/products/{id}
PUT    /api/products/{id}
DELETE /api/products/{id}
```

## Categories

``` text
GET  /api/categories
POST /api/categories
PUT  /api/categories/{id}
```

## Warehouses

``` text
GET  /api/warehouses
POST /api/warehouses
PUT  /api/warehouses/{id}
```

## Locations

``` text
GET  /api/locations
POST /api/locations
PUT  /api/locations/{id}
```

## Suppliers

``` text
GET  /api/suppliers
POST /api/suppliers
PUT  /api/suppliers/{id}
```

## Customers

``` text
GET  /api/customers
POST /api/customers
PUT  /api/customers/{id}
```

## Receipts

``` text
GET  /api/receipts
POST /api/receipts
GET  /api/receipts/{id}
POST /api/receipts/{id}/validate
POST /api/receipts/{id}/cancel
```

## Deliveries

``` text
GET  /api/deliveries
POST /api/deliveries
GET  /api/deliveries/{id}
POST /api/deliveries/{id}/pick
POST /api/deliveries/{id}/pack
POST /api/deliveries/{id}/validate
POST /api/deliveries/{id}/cancel
```

## Transfers

``` text
GET  /api/transfers
POST /api/transfers
GET  /api/transfers/{id}
POST /api/transfers/{id}/validate
POST /api/transfers/{id}/cancel
```

## Adjustments

``` text
GET  /api/adjustments
POST /api/adjustments
GET  /api/adjustments/{id}
POST /api/adjustments/{id}/validate
POST /api/adjustments/{id}/cancel
```

## Stock

``` text
GET /api/stock
GET /api/stock/{product_id}
GET /api/stock/{product_id}/locations
GET /api/stock/ledger
```

## Dashboard

``` text
GET /api/dashboard/summary
GET /api/dashboard/operations
GET /api/dashboard/low-stock
```

Add pagination, filtering, sorting, and search where appropriate.

------------------------------------------------------------------------

# 19. STATUS MODEL

Use:

``` text
DRAFT
WAITING
READY
DONE
CANCELED
```

Suggested flow:

``` text
DRAFT
  ↓
WAITING
  ↓
READY
  ↓
DONE
```

Cancellation can occur from appropriate pre-completion states.

DONE documents should be immutable from normal CRUD operations.

Do not allow a completed operation to be validated twice.

------------------------------------------------------------------------

# 20. FRONTEND

Create a professional inventory dashboard.

Required pages:

``` text
Login
Register
Forgot Password
Reset Password

Dashboard

Products
Product Details

Receipts
Receipt Details

Delivery Orders
Delivery Details

Internal Transfers
Transfer Details

Inventory Adjustments
Adjustment Details

Stock Ledger

Warehouses
Locations

Profile
```

Required UI states:

-   Loading
-   Empty
-   Error
-   Success
-   Form validation
-   Confirmation
-   Disabled actions
-   API failure

------------------------------------------------------------------------

# 21. DASHBOARD UI

Create KPI cards for:

``` text
Total Products
Low / Out of Stock
Pending Receipts
Pending Deliveries
Scheduled Transfers
```

Include useful operational information such as:

-   Recent movements
-   Low-stock products
-   Pending operations
-   Stock by location

Keep the UI clean and readable.

Avoid excessive animations.

------------------------------------------------------------------------

# 22. PRODUCT UI

Product list must support:

-   Search by name/SKU
-   Category filter
-   Stock status filter
-   Warehouse/location filter
-   Create product
-   Edit product
-   Product details
-   Stock distribution by location

------------------------------------------------------------------------

# 23. OPERATION UI

Each operation should have:

-   Document number
-   Status
-   Date
-   Warehouse
-   Location
-   Counterparty where applicable
-   Line items
-   Quantity
-   Action buttons
-   Validation confirmation
-   Error handling

Never show a successful validation before the backend confirms the
transaction.

------------------------------------------------------------------------

# 24. STOCK LEDGER UI

Display:

``` text
Date
Product
Warehouse
Location
Operation
Reference
Before
Change
After
User
Notes
```

Support:

-   Search
-   Product filter
-   Warehouse filter
-   Location filter
-   Operation type filter
-   Date filtering
-   Pagination

------------------------------------------------------------------------

# 25. SECURITY

Implement:

-   Password hashing
-   JWT/session security
-   Protected routes
-   Role checks where applicable
-   Input validation
-   SQLAlchemy parameterized queries
-   CORS configuration
-   OTP expiration
-   OTP attempt limits
-   Secure error messages
-   Environment-based secrets
-   No secret logging
-   No plaintext passwords

Do not expose stack traces to users in production mode.

------------------------------------------------------------------------

# 26. ROLES

Support at least:

``` text
INVENTORY_MANAGER
WAREHOUSE_STAFF
```

Inventory Manager may manage:

-   Products
-   Categories
-   Warehouses
-   Locations
-   Suppliers
-   Customers
-   Inventory operations
-   Dashboard

Warehouse Staff may perform operational work appropriate to warehouse
processes.

Enforce authorization on the backend, not only in the frontend.

------------------------------------------------------------------------

# 27. SEED DATA

Create development/demo seed data.

Example:

### Categories

``` text
Raw Materials
Finished Goods
Components
```

### UOM

``` text
Kilogram
Piece
Box
Meter
```

### Products

``` text
Steel Rods
Chairs
Bolts
Finished Frames
```

### Locations

``` text
Main Store
Production Rack
Rack A
Rack B
```

### Suppliers

Create realistic demo suppliers.

### Customers

Create realistic demo customers.

Create a development admin/inventory manager account through the seed
process.

Never commit a real password.

------------------------------------------------------------------------

# 28. DEMO FLOW

The completed system must support this demonstration:

## Step 1 --- Login

Login to StockSense.

## Step 2 --- Dashboard

Show current stock and pending operations.

## Step 3 --- Receive stock

Receive:

``` text
100 kg Steel Rods
```

Validate.

Expected:

``` text
Stock +100 kg
Ledger RECEIPT +100
```

## Step 4 --- Internal transfer

Transfer:

``` text
20 kg
Main Store → Production Rack
```

Expected:

``` text
Main Store -20
Production Rack +20
Total stock unchanged
```

## Step 5 --- Delivery

Deliver:

``` text
20 kg Steel Rods
```

Expected:

``` text
Total stock -20
Ledger DELIVERY -20
```

## Step 6 --- Adjustment

Physical count shows:

``` text
3 kg damaged
```

Adjust:

``` text
-3 kg
```

Expected:

``` text
Stock -3
Ledger ADJUSTMENT -3
```

## Step 7 --- Ledger

Show the complete history.

The judges should be able to see that every stock change is traceable.

------------------------------------------------------------------------

# 29. TESTING

Create tests for:

## Authentication

-   Register
-   Login
-   Invalid login
-   Password reset
-   Expired OTP
-   Used OTP
-   Unauthorized API access

## Products

-   Create
-   Read
-   Update
-   Duplicate SKU rejection

## Receipt

-   Create
-   Validate
-   Stock increase
-   Ledger creation
-   Duplicate validation rejection

## Delivery

-   Create
-   Pick
-   Pack
-   Validate
-   Stock decrease
-   Insufficient stock rejection

## Transfer

-   Valid transfer
-   Source decrease
-   Destination increase
-   Total stock invariant
-   Insufficient source stock rejection

## Adjustment

-   Positive adjustment
-   Negative adjustment
-   Ledger creation
-   Counted quantity becomes stock

## Ledger

Verify:

``` text
quantity_after = quantity_before + quantity_change
```

## Integration

Run the complete demo flow automatically.

------------------------------------------------------------------------

# 30. INVENTORY INVARIANTS

The following must always hold.

### Receipt

``` text
after = before + received
```

### Delivery

``` text
after = before - delivered
```

and:

``` text
delivered <= available
```

### Transfer

``` text
source_after = source_before - quantity
destination_after = destination_before + quantity
```

and:

``` text
total_before = total_after
```

### Adjustment

``` text
difference = counted - system
new_quantity = counted
```

### Ledger

``` text
after = before + change
```

Write automated tests for these invariants.

------------------------------------------------------------------------

# 31. DATABASE MIGRATIONS

Use Alembic.

Do not manually modify production database schema.

Create:

``` text
alembic/env.py
alembic/versions/001_initial_schema.py
```

The initial migration must create all required tables, constraints,
indexes, and relationships.

Verify:

``` bash
alembic upgrade head
```

Then verify the application starts.

------------------------------------------------------------------------

# 32. README

Create a complete `README.md` containing:

-   Project overview
-   Features
-   Architecture
-   Tech stack
-   Folder structure
-   Prerequisites
-   Environment variables
-   PostgreSQL setup
-   Backend setup
-   Frontend setup
-   Database migration
-   Seed instructions
-   Test instructions
-   Run instructions
-   API documentation location
-   Demo flow
-   Troubleshooting

A new developer should be able to clone the repository and run the
application from the README.

------------------------------------------------------------------------

# 33. ENVIRONMENT VARIABLES

Create `.env.example`.

Backend variables should include appropriate equivalents of:

``` text
DATABASE_URL=
JWT_SECRET=
JWT_ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
OTP_EXPIRE_MINUTES=
CORS_ORIGINS=
```

Do not put real secrets in `.env.example`.

------------------------------------------------------------------------

# 34. GITIGNORE

Include:

``` text
.env
.env.*
!.env.example

__pycache__/
*.py[cod]

.venv/
venv/
env/

.pytest_cache/
.mypy_cache/

node_modules/
dist/
build/

.coverage
htmlcov/

.vscode/
.idea/

*.log

.DS_Store
Thumbs.db
```

------------------------------------------------------------------------

# 35. DOCUMENTATION FILES

Generate:

## docs/problem.md

Document the StockSense problem statement.

## docs/requirements.md

Document:

-   Functional requirements
-   Non-functional requirements
-   Users
-   Features
-   Acceptance criteria
-   P0/P1/P2 scope

## docs/architecture.md

Document:

``` text
React
   ↓
FastAPI
   ↓
Services
   ↓
Repositories / SQLAlchemy
   ↓
PostgreSQL
```

## docs/database.md

Document:

-   ER model
-   Tables
-   Relationships
-   Constraints
-   Indexes
-   Transaction rules

## docs/api.md

Document endpoints and request/response structures.

## docs/authentication.md

Document login and OTP reset flow.

## docs/inventory-engine.md

Document stock-changing business logic.

## docs/stock-ledger.md

Document ledger invariants and transaction history.

## docs/security.md

Document security controls.

## docs/testing.md

Document test strategy.

## docs/deployment.md

Document local and deployment setup.

## docs/demo-script.md

Document the hackathon demo sequence.

------------------------------------------------------------------------

# 36. AGENT RULE FILES

Create rules that reinforce:

### global.md

-   Read project documentation first.
-   Preserve architecture.
-   Test every change.
-   Never commit secrets.
-   Never fake backend data.

### backend.md

-   Use FastAPI.
-   Use service-layer business logic.
-   Validate inputs.
-   Use transactions for stock operations.

### frontend.md

-   Use TypeScript.
-   Use reusable components.
-   Handle loading/error/empty states.
-   Never hard-code business data.

### database.md

-   PostgreSQL is authoritative.
-   Use migrations.
-   Preserve foreign-key integrity.
-   Use transaction locking for stock changes.

### security.md

-   Never expose secrets.
-   Hash passwords.
-   Validate authorization server-side.
-   Protect OTP flow.

### testing.md

-   Every P0 feature requires tests.
-   Test inventory invariants.
-   Run tests after changes.

### git.md

-   Make small meaningful commits.
-   Do not commit generated secrets.
-   Do not rewrite shared history without approval.

------------------------------------------------------------------------

# 37. BUILD ORDER

Follow this exact order unless an existing repository requires a safe
variation.

## Phase 1 --- Repository foundation

Create:

``` text
README.md
.gitignore
.env.example
.agents/
docs/
```

Verify Git state.

## Phase 2 --- Backend foundation

Create:

``` text
backend/
FastAPI
configuration
database connection
SQLAlchemy base
Alembic
```

Run application health check.

## Phase 3 --- Database

Create:

``` text
all SQLAlchemy models
relationships
constraints
indexes
initial Alembic migration
```

Run:

``` bash
alembic upgrade head
```

Verify schema.

## Phase 4 --- Authentication

Implement:

``` text
register
login
logout
current user
forgot password
OTP reset
authorization
```

Write tests.

## Phase 5 --- Master data

Implement:

``` text
categories
UOM
products
warehouses
locations
suppliers
customers
```

Write tests.

## Phase 6 --- Inventory engine

Implement:

``` text
stock balance
ledger
receipt
delivery
transfer
adjustment
```

Write invariant tests.

This is the most important backend phase.

## Phase 7 --- Dashboard

Implement dashboard APIs.

## Phase 8 --- Frontend

Create:

``` text
React
routing
authentication
layout
dashboard
products
operations
ledger
settings
profile
```

## Phase 9 --- Integration

Connect frontend to real backend.

Remove all mock data.

## Phase 10 --- Testing

Run:

``` text
backend tests
frontend tests
integration tests
type checks
lint
```

Fix all failures.

## Phase 11 --- UI refinement

Verify:

-   Responsive layout
-   Navigation
-   Loading states
-   Empty states
-   Error messages
-   Confirmation dialogs
-   Tables
-   Forms
-   Consistent typography
-   Consistent spacing

## Phase 12 --- Demo preparation

Seed demo data.

Run the full demo flow.

Verify every stock number.

------------------------------------------------------------------------

# 38. COMMANDS TO VERIFY

The exact commands may differ depending on environment, but verify
equivalents of:

### Backend

``` bash
python -m venv .venv
pip install -r backend/requirements.txt
alembic upgrade head
pytest
```

### Frontend

``` bash
npm install
npm run build
```

If lint is configured:

``` bash
npm run lint
```

### Application

Run backend and frontend.

Verify:

``` text
GET /health
```

returns a successful response.

------------------------------------------------------------------------

# 39. HEALTH ENDPOINT

Implement:

``` text
GET /health
```

Response should contain a simple successful status and should not expose
secrets.

------------------------------------------------------------------------

# 40. ERROR HANDLING

Use consistent API errors.

Example:

``` json
{
  "detail": "Insufficient stock"
}
```

Do not expose:

-   SQL queries
-   passwords
-   stack traces
-   internal credentials
-   environment variables

------------------------------------------------------------------------

# 41. API DOCUMENTATION

FastAPI's OpenAPI documentation should work.

Verify:

``` text
/docs
/redoc
```

Do not disable documentation for local development.

------------------------------------------------------------------------

# 42. CODE QUALITY

Follow:

-   Type hints in Python
-   TypeScript types
-   Clear function names
-   Small functions
-   Single responsibility
-   Reusable components
-   Meaningful error messages
-   No dead code
-   No unnecessary dependencies
-   No duplicated inventory logic

------------------------------------------------------------------------

# 43. NO FAKE IMPLEMENTATION RULE

The following are prohibited in the final P0 implementation:

``` python
return {"products": []}
```

when real database retrieval is required.

``` typescript
const products = [...]
```

when the page should retrieve products from the API.

Fake dashboard numbers.

Fake successful validation.

Fake stock updates only in frontend state.

The UI must reflect the actual PostgreSQL state.

------------------------------------------------------------------------

# 44. FAILURE RECOVERY

If a tool/agent reaches a limit or stops unexpectedly:

1.  Stop at the last safe point.
2.  Save current task state.
3.  Run tests.
4.  Record errors.
5.  Commit a checkpoint if safe.
6.  Write a handoff file in `.agents/handoffs/`.
7.  A replacement agent must read:
    -   `WORKFLOW.md`
    -   `BUILD_STOCKSENSE.md`
    -   relevant `.agents/rules/*`
    -   current task
    -   latest handoff
8.  Verify the current state before continuing.

Never assume previous work completed successfully.

------------------------------------------------------------------------

# 45. TASK TRACKING

Create task files as implementation progresses.

Example:

``` text
.agents/tasks/001-project-foundation.md
.agents/tasks/002-database.md
.agents/tasks/003-authentication.md
...
```

Each task should contain:

``` markdown
# Task

## Objective

## Files

## Requirements

## Acceptance Criteria

## Verification

## Status
```

Mark tasks complete only after verification.

------------------------------------------------------------------------

# 46. FINAL DEFINITION OF DONE

The project is considered complete only when all of these are true:

-   [ ] Repository structure exists
-   [ ] README exists
-   [ ] Environment example exists
-   [ ] PostgreSQL connection works
-   [ ] Alembic migration works
-   [ ] All required tables exist
-   [ ] Foreign keys work
-   [ ] Unique constraints work
-   [ ] Authentication works
-   [ ] OTP reset works
-   [ ] Products work
-   [ ] Warehouses work
-   [ ] Locations work
-   [ ] Suppliers work
-   [ ] Customers work
-   [ ] Receipts work
-   [ ] Deliveries work
-   [ ] Transfers work
-   [ ] Adjustments work
-   [ ] Stock balances update correctly
-   [ ] Stock ledger records every movement
-   [ ] Inventory invariants pass
-   [ ] Dashboard displays real data
-   [ ] Search works
-   [ ] Filters work
-   [ ] Frontend is connected to backend
-   [ ] No P0 mock data remains
-   [ ] Backend tests pass
-   [ ] Frontend build passes
-   [ ] Integration flow passes
-   [ ] No secrets are committed
-   [ ] Documentation is complete
-   [ ] Demo flow works from start to finish

------------------------------------------------------------------------

# 47. FINAL DEMO VALIDATION

Before declaring completion, execute this exact scenario against the
real database:

``` text
1. Login
2. Open dashboard
3. Record current Steel Rod stock
4. Receive +100 kg
5. Validate receipt
6. Verify stock increased by exactly 100
7. Verify receipt ledger entry
8. Transfer 20 kg Main Store → Production Rack
9. Verify source decreased by 20
10. Verify destination increased by 20
11. Verify total stock unchanged
12. Deliver 20 kg
13. Verify total stock decreased by 20
14. Adjust -3 kg for damage
15. Verify final stock
16. Open ledger
17. Verify all movements and before/after values
18. Refresh the page
19. Verify data persists from PostgreSQL
20. Log out
21. Verify protected pages require authentication
```

The system must pass this flow using real API calls and PostgreSQL data.

------------------------------------------------------------------------

# 48. EXECUTION INSTRUCTION

Now execute this specification.

Start by inspecting the repository.

Then:

``` text
1. Create missing directory structure.
2. Create documentation.
3. Create backend foundation.
4. Create database models.
5. Create Alembic migration.
6. Create database.
7. Create authentication.
8. Create master-data APIs.
9. Create inventory engine.
10. Create stock ledger.
11. Create operation APIs.
12. Create dashboard APIs.
13. Create React frontend.
14. Connect frontend to APIs.
15. Create tests.
16. Run migrations.
17. Seed development data.
18. Run tests.
19. Fix failures.
20. Run build.
21. Run complete demo flow.
22. Update README.
23. Report final status.
```

After every major phase, verify the implementation before moving
forward.

If something fails, **fix the root cause instead of bypassing the
test**.

At the end, report:

``` text
PROJECT STATUS
---------------
Backend: PASS/FAIL
Database: PASS/FAIL
Migration: PASS/FAIL
Authentication: PASS/FAIL
Products: PASS/FAIL
Receipts: PASS/FAIL
Deliveries: PASS/FAIL
Transfers: PASS/FAIL
Adjustments: PASS/FAIL
Stock Ledger: PASS/FAIL
Dashboard: PASS/FAIL
Frontend: PASS/FAIL
Tests: PASS/FAIL
Build: PASS/FAIL
Demo Flow: PASS/FAIL

Remaining Issues:
- ...

Next Recommended Action:
- ...
```

Do not claim PASS unless the relevant verification actually succeeded.


---

# 49. WIREFRAME-DRIVEN UI/UX REFINEMENT

The supplied StockSense wireframes are the visual and interaction reference for the application.

The wireframes define the intended **information architecture, navigation, fields, status behavior, list views, detail views, and user flows**. They are not a requirement to reproduce the hand-drawn visual style literally.

Build a polished production-quality UI that preserves the intent of the wireframes.

## 49.1 Visual direction

Use a modern dark inventory-management interface inspired by the wireframes:

- Dark application background.
- High-contrast content surfaces.
- Coral/pink primary accent.
- Clear white/light text.
- Subtle borders.
- Compact but readable tables.
- Rounded cards and controls.
- Consistent iconography.
- Responsive desktop-first layout.
- Clear hover/focus/active states.
- Minimal animation.
- No unnecessary gradients or visual clutter.

Use centralized design tokens rather than scattering colors throughout components.

Example semantic tokens:

```text
--background
--surface
--surface-elevated
--border
--text-primary
--text-secondary
--accent
--success
--warning
--danger
```

The exact values may be refined during implementation, but the overall dark + coral visual language should remain recognizable.

---

# 50. APPLICATION NAVIGATION

The primary application navigation should follow the wireframes:

```text
Dashboard
Operations
Stock
Products
Move History
Settings
```

A user/profile control should appear in the application header.

## Operations submenu

```text
Receipts
Delivery Orders
Internal Transfers
Inventory Adjustments
```

## Settings submenu

```text
Warehouses
Locations
```

## Profile menu

```text
My Profile
Logout
```

Navigation must be responsive.

On smaller screens:

- Collapse the sidebar/navigation.
- Preserve access to every page.
- Do not hide required operations behind inaccessible UI.

---

# 51. AUTHENTICATION WIREFRAME REQUIREMENTS

The authentication screens should follow the supplied Login/Signup wireframe.

## 51.1 Login page

Display:

```text
App Logo

Login ID
Password

SIGN IN

Forgot Password? | Sign Up
```

Requirements:

- Login ID is required.
- Password is required.
- Sign In validates credentials through the backend.
- Invalid credentials display a clear error.
- Successful login redirects to Dashboard.
- Sign Up navigates to the registration page.
- Forgot Password navigates to password reset.
- Do not expose whether a specific account exists through unsafe error messages.
- Password input must be masked.
- Provide show/hide password control if it improves usability.

## 51.2 Signup page

Display:

```text
App Logo

Login ID
Email ID
Password
Re-enter Password

SIGN UP
```

Validation:

### Login ID

- Required.
- Unique.
- Length: 6–12 characters.
- Allow only a documented safe character set.
- Reject duplicates.

### Email

- Required.
- Valid email format.
- Unique.

### Password

Minimum 8 characters.

Must contain:

- at least one lowercase letter,
- at least one uppercase letter,
- at least one special character.

The implementation may additionally require a digit if clearly documented, but do not make password rules stricter than necessary without updating the UI documentation.

### Confirm password

Must exactly match the password.

All validation must exist on both:

```text
Frontend
Backend
```

The backend is authoritative.

---

# 52. AUTHENTICATION DATABASE REFINEMENT

Update the `users` model to include:

```text
id
login_id UNIQUE
full_name
email UNIQUE
password_hash
role
is_active
created_at
updated_at
last_login_at
```

`login_id` is the identifier used by the login form.

Do not remove email uniqueness.

Update authentication APIs and schemas accordingly.

Login request:

```json
{
  "login_id": "...",
  "password": "..."
}
```

Registration request:

```json
{
  "login_id": "...",
  "email": "...",
  "password": "...",
  "confirm_password": "..."
}
```

Do not store `confirm_password`.

---

# 53. STOCK PAGE — WIREFRAME REQUIREMENTS

Create a dedicated **Stock** page.

The page should display a table similar in information density to the supplied wireframe.

Required columns:

```text
Product
Per Unit Cost
On Hand
Free to Use
```

Recommended additional columns where space permits:

```text
SKU
Category
Warehouse
Location
Stock Status
```

## 53.1 Meaning of stock quantities

### On Hand

Physical quantity currently held in the selected stock location.

### Reserved

Quantity committed to pending/ready outgoing operations.

### Free to Use

```text
free_to_use = on_hand - reserved
```

Never allow:

```text
free_to_use < 0
```

unless an explicit administrative override is implemented.

## 53.2 Stock balance refinement

Extend `stock_balances` with:

```text
quantity
reserved_quantity
updated_at
```

Use:

```text
on_hand = quantity
free_to_use = quantity - reserved_quantity
```

Do not persist `free_to_use` as an independent source-of-truth value unless there is a strong database reason.

Calculate it consistently in the backend response.

---

# 54. STOCK RESERVATION BEHAVIOR

The wireframe's "Waiting" state represents an operation waiting for required stock.

Implement this behavior carefully.

For a delivery:

### Draft

No stock reservation.

### Waiting

The requested stock is not currently available.

```text
free_to_use < requested_quantity
```

Do not allow final validation.

### Ready

Required stock is available.

Reserve the required quantity when the operation becomes Ready if the application workflow supports explicit readiness/reservation.

```text
reserved_quantity += requested_quantity
```

### Done

On successful final validation:

```text
quantity -= delivered_quantity
reserved_quantity -= delivered_quantity
```

Create the ledger entry.

### Canceled

If stock was reserved:

```text
reserved_quantity -= reserved_amount
```

No physical stock reduction occurs.

All reservation changes must be transactional.

If the team chooses not to implement persistent reservation during the hackathon, `reserved_quantity` may remain zero and Waiting must still be determined from `free_to_use`. However, the API and UI must not claim that stock is reserved when it is not.

---

# 55. STOCK UPDATE ENTRY POINT

The Stock page must allow users to initiate stock-related operations from the relevant product row.

For example:

```text
Product | On Hand | Free to Use | Actions
Desk    | 50      | 45          | View | Receive | Deliver | Transfer | Adjust
```

The exact action set can depend on user role.

Do not directly mutate stock from the frontend.

Every stock-changing action must call the appropriate backend operation:

```text
Receive
Delivery
Transfer
Adjustment
```

The Stock page is a convenient entry point, not a bypass around the inventory engine.

---

# 56. WAREHOUSE AND LOCATION MANAGEMENT

The supplied wireframes show dedicated Warehouse and Location forms.

## 56.1 Warehouse

Display:

```text
Warehouse

Name
Short Code
Address

Save
Cancel
```

Database mapping:

```text
name
code
address
```

The short code is the warehouse code.

Warehouse code must be unique.

## 56.2 Location

Display:

```text
Location

Name
Short Code
Warehouse

Save
Cancel
```

The selected warehouse is required.

Location code must be unique within a warehouse.

Database constraint:

```text
UNIQUE(warehouse_id, code)
```

A location belongs to exactly one warehouse.

---

# 57. OPERATION REFERENCE NUMBERING

The supplied wireframes use references such as:

```text
WH/IN/0001
WH/OUT/0001
WH/INT/0001
WH/ADJ/0001
```

Implement a centralized reference-number generator.

Use these prefixes:

```text
Receipt      → WH/IN/
Delivery     → WH/OUT/
Transfer     → WH/INT/
Adjustment   → WH/ADJ/
```

Example:

```text
WH/IN/0001
WH/IN/0002

WH/OUT/0001
WH/OUT/0002

WH/INT/0001

WH/ADJ/0001
```

Requirements:

- Generated by backend.
- Never generated by frontend.
- Unique.
- Collision-safe under concurrent requests.
- Human-readable.
- Do not reuse a reference after cancellation.
- Do not depend on the frontend to calculate the next number.

Create a dedicated numbering service.

---

# 58. RECEIPT LIST VIEW

The Receipts page should open by default in **List View**.

Header:

```text
NEW    Receipts
```

Toolbar:

```text
Search
List View
Kanban View
```

Required columns:

```text
Reference
From
To
Contact
Schedule Date
Status
```

The list must be populated from real backend data.

Support:

- Search by reference.
- Search by contact.
- Filter by status.
- Filter by warehouse.
- Filter by date.
- Sort by schedule date.
- Pagination.

If one receipt contains multiple products, the list remains one document row. Product-level information belongs in the detail page unless a specific grouped display is required.

---

# 59. RECEIPT DETAIL VIEW

Clicking a receipt opens its detail page.

Header:

```text
NEW / Receipt
Validate
Print
Cancel
```

Status progress:

```text
Draft → Ready → Done
```

The application may use Waiting where stock/dependency logic requires it.

Display:

```text
Reference

Receive From
Schedule Date
Responsible
Operation Type

Products
Product
Quantity
UOM
```

Responsible should automatically use the currently authenticated user when creating a new receipt unless an authorized user explicitly changes it.

Example:

```text
WH/IN/0001
```

A receipt cannot be marked Done until backend validation succeeds.

The Print action should generate a clean printable receipt document once the operation is sufficiently complete.

---

# 60. DELIVERY LIST VIEW

The Delivery page should open by default in **List View**.

Header:

```text
NEW    Delivery
```

Toolbar:

```text
Search
List View
Kanban View
```

Required columns:

```text
Reference
From
To
Contact
Schedule Date
Status
```

Example reference:

```text
WH/OUT/0001
```

Support:

- Search by reference.
- Search by contact/customer.
- Status filtering.
- Warehouse/location filtering.
- Date filtering.
- Sorting.
- Pagination.

---

# 61. DELIVERY DETAIL VIEW

Display:

```text
Reference

Delivery Address
Schedule Date
Responsible
Operation Type

Products
Product
Quantity

Validate
Print
Cancel
```

Status pipeline:

```text
Draft → Waiting → Ready → Done
```

Meaning:

```text
Draft:
Initial editable state.

Waiting:
Required stock is not currently available.

Ready:
Required stock is available and the operation can be completed.

Done:
Stock has been successfully deducted and the ledger has been written.

Canceled:
Operation is canceled and cannot be completed.
```

The UI must not allow Validate when the backend reports insufficient stock.

Display a clear error such as:

```text
Insufficient stock for this delivery.
Available: 5
Requested: 10
```

Do not expose internal database errors.

---

# 62. DELIVERY STATUS AND DATE LOGIC

The wireframes distinguish operational states and late operations.

Implement:

## Late

An operation is Late when:

```text
schedule_date < current_time
AND status NOT IN (DONE, CANCELED)
```

## Future / Scheduled

An operation is scheduled when:

```text
schedule_date > current_time
AND status NOT IN (DONE, CANCELED)
```

## Waiting

An operation is Waiting when it cannot proceed because required stock is unavailable.

The backend should calculate business state where possible.

The frontend should not independently invent a different definition.

Use the server-provided status/state for dashboard counts.

---

# 63. DASHBOARD WIREFRAME REFINEMENT

The dashboard should visually follow the supplied wireframe.

Primary operational cards:

```text
Receipt
Delivery
```

Each card should show information such as:

```text
X to receive
Y late
Z waiting
N operations
```

and:

```text
X to deliver
Y late
Z waiting
N operations
```

Make the entire action area clickable.

For example:

```text
4 to receive
```

opens the Receipts page filtered to relevant pending receipts.

```text
4 to deliver
```

opens Delivery Orders filtered to relevant pending deliveries.

---

# 64. DASHBOARD COUNTS

Create backend dashboard calculations.

For receipts:

```text
to_receive
late
waiting
operations
```

For deliveries:

```text
to_deliver
late
waiting
operations
```

Definitions:

### operations

Count relevant non-finalized operation documents.

### late

Count documents satisfying:

```text
schedule_date < now
AND status NOT IN (DONE, CANCELED)
```

### waiting

Count documents whose current business state is Waiting.

### to_receive / to_deliver

Count relevant pending documents that require action.

Do not hard-code these numbers.

---

# 65. DASHBOARD ADDITIONAL INFORMATION

In addition to the main Receipt and Delivery cards, provide:

```text
Total Products
Low Stock / Out of Stock
Scheduled Transfers
Recent Stock Movements
```

The dashboard should remain concise.

Do not turn it into an analytics-heavy page.

The goal is to help a warehouse user immediately answer:

```text
What needs my attention?
What stock do I have?
What is late?
What is waiting?
What moved recently?
```

---

# 66. MOVE HISTORY

Create a dedicated **Move History** page.

The wireframe uses a table with:

```text
Reference
Date
Contact
From
To
Quantity
Status
```

Implement those fields.

Example:

```text
WH/IN/0001
WH/OUT/0002
WH/INT/0001
```

Search must support:

```text
Reference
Contact
```

Recommended additional filters:

```text
Operation Type
Status
Warehouse
Location
Date Range
Product
```

---

# 67. MULTI-PRODUCT MOVE HISTORY

If a single reference contains multiple products, display multiple rows when the move-history view is product-specific.

Example:

```text
WH/OUT/0002 | Desk  | 10 | ...
WH/OUT/0002 | Chair | 5  | ...
```

Do not create duplicate database operation documents merely to produce multiple display rows.

The underlying document remains one operation with multiple items.

---

# 68. MOVE HISTORY VIEW MODES

Support:

```text
List View
Kanban View
```

List View is the default.

Kanban View groups operations by status.

For example:

```text
Draft
Waiting
Ready
Done
Canceled
```

Each Kanban card should show:

```text
Reference
Contact
Schedule Date
Quantity / item summary
Status
```

Clicking a card opens the underlying operation detail.

The list/Kanban toggle changes presentation only; it must not alter business logic.

---

# 69. SEARCH BEHAVIOR

Search should be available where shown in the wireframes.

At minimum support:

### Products

```text
Name
SKU
```

### Receipts

```text
Reference
Contact / Supplier
```

### Deliveries

```text
Reference
Contact / Customer
```

### Move History

```text
Reference
Contact
```

Search must be server-backed for large datasets.

Use debouncing in the frontend where appropriate.

---

# 70. OPERATION TYPE

The detail screens show an Operation Type field.

Implement a controlled enum:

```text
IN
OUT
INTERNAL
ADJUSTMENT
```

Mappings:

```text
Receipt → IN
Delivery → OUT
Transfer → INTERNAL
Adjustment → ADJUSTMENT
```

Do not allow users to change the operation type into an incompatible operation.

The operation type is derived from the document type where possible.

---

# 71. PRINTING

Support a clean printable representation for completed or printable operation documents.

At minimum:

```text
Reference
Operation Type
Date
Warehouse
Location
Responsible
Contact
Products
Quantities
Status
```

The printed representation should be suitable for:

- PDF printing from browser
- physical warehouse records
- demo presentation

Do not introduce a complex document-generation service unless required.

---

# 72. OPERATION FORMS

All operation forms should support adding/removing product lines.

Example:

```text
Products
--------------------------------
Product       Quantity      UOM
Desk          10            Unit
Chair         5             Unit

+ Add Product
```

Prevent:

- zero quantity,
- negative quantity,
- missing product,
- invalid UOM,
- duplicate lines unless explicitly merged,
- invalid warehouse/location combinations.

---

# 73. RESPONSIBLE USER

For newly created operations:

```text
Responsible = current authenticated user
```

Display the responsible user in the detail view.

Store the user ID in the database.

Do not trust a frontend-supplied arbitrary user ID for authorization.

An authorized manager may reassign responsibility if that feature is implemented.

---

# 74. WAREHOUSE/LOCATION RELATIONSHIP RULES

Enforce:

```text
Location belongs to Warehouse.
Stock belongs to Location.
Location determines Warehouse.
```

A transfer:

```text
source_location
destination_location
```

must validate both locations.

For a same-warehouse transfer:

```text
warehouse(source) == warehouse(destination)
```

For a cross-warehouse transfer:

```text
warehouse(source) != warehouse(destination)
```

The system must support both.

The transfer ledger must record the correct warehouse/location for both sides.

---

# 75. STOCK LOCATION VIEW

When a user opens a product, show:

```text
Product
SKU
Category
UOM

Stock Summary

Warehouse | Location | On Hand | Reserved | Free to Use
```

This makes the multi-location behavior visible.

The total stock of a product should be calculable as:

```text
SUM(on_hand across locations)
```

Do not double-count transfers.

---

# 76. LOW-STOCK RULE

A product/location is low-stock when:

```text
free_to_use <= reorder_level
```

or, if reorder rules are configured:

```text
free_to_use <= reorder_rule.minimum_quantity
```

Out of stock:

```text
free_to_use <= 0
```

The dashboard and stock UI should distinguish:

```text
Healthy
Low Stock
Out of Stock
```

Do not use only frontend color to communicate status; include text/badges for accessibility.

---

# 77. STATUS COLOR SEMANTICS

Use consistent semantic styling:

```text
Done       → success
Ready      → accent/info
Waiting    → warning
Draft      → neutral
Canceled   → danger/neutral
Late       → danger
Low Stock  → warning
Out Stock  → danger
```

Do not rely solely on color.

Every status should have text.

---

# 78. WIREFRAME ACCEPTANCE CRITERIA

The implementation is considered UI-complete when:

- [ ] Login screen follows the supplied login structure.
- [ ] Signup screen follows the supplied signup structure.
- [ ] Login ID validation works.
- [ ] Email validation works.
- [ ] Password complexity works.
- [ ] Dashboard follows the supplied operational-card structure.
- [ ] Receipt list exists.
- [ ] Receipt detail exists.
- [ ] Delivery list exists.
- [ ] Delivery detail exists.
- [ ] Stock page exists.
- [ ] Stock table includes On Hand and Free to Use.
- [ ] Warehouse form exists.
- [ ] Location form exists.
- [ ] Move History exists.
- [ ] Move History supports search.
- [ ] Move History supports List/Kanban presentation.
- [ ] Operations support status progression.
- [ ] Late state is calculated correctly.
- [ ] Waiting state is calculated correctly.
- [ ] Operation references follow the required format.
- [ ] Responsible user is populated from authenticated user.
- [ ] Search controls are functional.
- [ ] Print action works for supported operation documents.
- [ ] All displayed inventory values come from PostgreSQL.
- [ ] UI is responsive.
- [ ] UI has loading/error/empty states.

---

# 79. WIREFRAME-TO-DATABASE MAPPING

The agent must ensure the UI requirements have corresponding backend data.

| UI Requirement | Backend/Data Source |
|---|---|
| Login ID | `users.login_id` |
| Email | `users.email` |
| Warehouse | `warehouses` |
| Location | `locations` |
| Stock | `stock_balances` |
| On Hand | `stock_balances.quantity` |
| Reserved | `stock_balances.reserved_quantity` |
| Free to Use | `quantity - reserved_quantity` |
| Product | `products` |
| Receipt | `receipts` + `receipt_items` |
| Delivery | `deliveries` + `delivery_items` |
| Transfer | `transfers` + `transfer_items` |
| Adjustment | `adjustments` + `adjustment_items` |
| Move History | operation documents + `stock_ledger` |
| Responsible | `created_by` / responsible user FK |
| Schedule Date | operation `scheduled_at` |
| Contact | supplier/customer |
| Operation Type | derived operation enum |
| Status | operation status/state |
| Late | backend-derived state |
| Waiting | backend-derived business state |
| Dashboard counts | dashboard service |

---

# 80. SCHEMA OVERRIDES FROM WIREFRAMES

The following refinements override earlier generic definitions in this document.

## users

Use:

```text
id
login_id UNIQUE NOT NULL
full_name
email UNIQUE NOT NULL
password_hash NOT NULL
role
is_active
created_at
updated_at
last_login_at
```

## stock_balances

Use:

```text
id
product_id
location_id
quantity
reserved_quantity
updated_at
```

Constraints:

```text
UNIQUE(product_id, location_id)
quantity >= 0
reserved_quantity >= 0
reserved_quantity <= quantity
```

If the business flow temporarily requires a reservation to exceed currently available physical stock, do not violate the constraint silently. Instead, prevent the reservation.

## Operation documents

Add or ensure:

```text
reference_number
scheduled_at
created_by
responsible_user_id
status
```

If `created_by` and `responsible_user_id` are semantically identical in the implementation, one FK may be sufficient, but the API should still expose a clear `responsible` concept.

## Operation items

Every operation item must contain:

```text
product_id
quantity
uom_id
```

---

# 81. BACKEND RESPONSE CONTRACTS FOR UI

The frontend should not reconstruct important business state.

For stock, return fields equivalent to:

```json
{
  "product_id": 1,
  "product_name": "Desk",
  "sku": "DESK001",
  "warehouse_id": 1,
  "warehouse_name": "Main Warehouse",
  "location_id": 1,
  "location_name": "WH/Stock",
  "on_hand": 50,
  "reserved": 5,
  "free_to_use": 45,
  "stock_status": "HEALTHY"
}
```

For operations, return fields equivalent to:

```json
{
  "reference": "WH/OUT/0001",
  "operation_type": "OUT",
  "status": "READY",
  "business_state": "READY",
  "scheduled_at": "...",
  "responsible": {
    "id": 1,
    "login_id": "..."
  },
  "contact": "...",
  "from": "...",
  "to": "...",
  "is_late": false,
  "is_waiting": false
}
```

The exact JSON structure may vary, but the semantic fields must be available.

---

# 82. UI STATE RULE

Do not derive critical business state using separate frontend logic.

The backend is authoritative for:

```text
available stock
free to use
waiting
late
operation status
permission
validation result
```

The frontend may format and display these values.

---

# 83. REFINED HACKATHON PRIORITY

Because the wireframes add several user-facing requirements, update priority as follows.

## P0 — Must work

```text
Authentication
Dashboard
Stock
Products
Warehouses
Locations
Receipts
Delivery Orders
Internal Transfers
Inventory Adjustments
Move History
Stock Ledger
Search
Status workflow
Real PostgreSQL persistence
Transaction-safe stock updates
```

## P1 — Important polish

```text
Kanban View
Printing
Advanced filtering
Low-stock alerts
Role refinement
Responsive refinement
Better dashboard interactions
```

## P2 — Optional

```text
Advanced analytics
Barcode scanning
CSV import/export
Predictive replenishment
AI assistant
Advanced notifications
```

Do not start P2 work while a P0 feature is broken.

---

# 84. REFINED DEMO FLOW

Use the wireframe-oriented flow for the final hackathon demo:

```text
1. Open Login
2. Sign in using Login ID + password
3. Land on Dashboard
4. Show Receipt and Delivery operational cards
5. Open Stock
6. Show Product / On Hand / Free to Use
7. Open Products
8. Create or inspect a product
9. Open Warehouse settings
10. Show warehouse and locations
11. Create a receipt
12. Show WH/IN/0001-style reference
13. Validate receipt
14. Return to Stock
15. Verify On Hand increased
16. Open Move History
17. Verify receipt movement
18. Create an internal transfer
19. Verify source and destination
20. Create a delivery
21. Show Waiting if stock is insufficient
22. Add/receive stock if required
23. Move delivery to Ready
24. Validate delivery
25. Verify On Hand and Free to Use
26. Perform an adjustment
27. Open Move History
28. Switch List → Kanban
29. Search by reference/contact
30. Open completed operation
31. Print the operation
32. Return to Dashboard
33. Show updated operational counts
```

---

# 85. FINAL WIREFRAME VALIDATION

Before declaring the project complete, the agent must inspect every implemented screen against the supplied wireframe requirements.

Verify:

```text
Authentication
Dashboard
Stock
Warehouse
Location
Move History
Delivery List
Delivery Detail
Receipt List
Receipt Detail
```

For every screen verify:

```text
Layout
Navigation
Fields
Buttons
Search
Status
Data
Validation
Loading
Empty State
Error State
Responsive behavior
```

The agent must not claim visual completion merely because the application compiles.

---

# 86. UPDATED EXECUTION RULE

The original implementation sequence remains valid, but after the backend foundation and database phase, the agent must incorporate the wireframe refinements before final frontend integration.

Updated sequence:

```text
1. Repository inspection
2. Documentation and agent rules
3. Backend foundation
4. Database schema
5. Authentication
6. Master data
7. Inventory engine
8. Operation APIs
9. Dashboard APIs
10. Stock APIs
11. Move History APIs
12. Frontend shell/navigation
13. Authentication UI
14. Dashboard UI
15. Stock UI
16. Products UI
17. Warehouse/Location UI
18. Receipt UI
19. Delivery UI
20. Transfer UI
21. Adjustment UI
22. Move History UI
23. List/Kanban views
24. Search/filtering
25. Printing
26. Full integration
27. Automated testing
28. UI refinement
29. Demo validation
30. Final documentation
```

At every stage, preserve the central rule:

```text
UI action
    ↓
API
    ↓
Service
    ↓
Transactional database operation
    ↓
Stock balance
    ↓
Stock ledger
    ↓
Updated UI
```

There must never be a separate frontend-only inventory state.

---

# 87. FINAL QUALITY BAR

The completed StockSense application should feel like a coherent inventory product, not a collection of disconnected CRUD pages.

A warehouse user should be able to understand:

```text
Where is my stock?
How much is physically available?
How much is free to use?
What needs to be received?
What needs to be delivered?
What is waiting?
What is late?
Where did stock move?
Who performed the operation?
When did it happen?
Can I trace the change?
```

The implementation must answer those questions using real PostgreSQL-backed data.

Do not optimize for the number of files created.

Optimize for:

```text
Correctness
Traceability
Usability
Data integrity
Fast workflow
Clear UI
Reliable demo
```
