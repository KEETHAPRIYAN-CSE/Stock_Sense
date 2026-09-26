# StockSense --- AI Hackathon Development Workflow

**Version:** 1.0\
**Project:** StockSense --- Modular Inventory Management System\
**Purpose:** Single source of truth for human developers and AI coding
agents\
**Primary stack:** React + TypeScript + Vite, FastAPI + Python,
SQLAlchemy, PostgreSQL 18, Git/GitHub\
**AI tooling:** Google Antigravity, Cursor, Codex

------------------------------------------------------------------------

# 0. Operating Principle

StockSense is an inventory transaction system first and a dashboard
second.

The core invariant is:

> Every stock-changing operation must be validated, persisted
> transactionally, and represented in the stock ledger.

The system must replace manual registers, Excel sheets, and scattered
tracking with a centralized, real-time, easy-to-use inventory
application.

Target users:

-   Inventory Managers --- manage incoming and outgoing stock.
-   Warehouse Staff --- perform transfers, picking, shelving, and
    counting.

The source problem statement explicitly requires authentication, a
dashboard, products, receipts, delivery orders, inventory adjustments,
move history, warehouse settings, profile/logout, stock alerts,
multi-warehouse support, SKU search, and smart filters.

------------------------------------------------------------------------

# 1. AI Execution Contract

All AI agents MUST follow this document.

AI agents MUST:

1.  Read this file before changing the project.
2.  Identify the current development level.
3.  Read the relevant task file.
4.  Inspect existing code before creating new code.
5.  Reuse existing architecture and components.
6.  Avoid unnecessary dependencies.
7.  Never expose secrets.
8.  Never silently change database schema.
9.  Never bypass validation.
10. Never modify unrelated modules.
11. Run relevant tests after implementation.
12. Update task state before handing work to another agent.
13. Commit meaningful checkpoints to Git.
14. Report assumptions explicitly.
15. Stop and ask for human approval for architecture changes,
    destructive database changes, authentication/security changes,
    deployment changes, or major dependency changes.

AI agents must prefer a small, complete, testable implementation over a
large unfinished feature set.

------------------------------------------------------------------------

# 2. Development Levels

Every request belongs to one of these levels.

## Level 1 --- Concept & Scope

Goal:

-   Understand the problem.
-   Identify users.
-   Extract requirements.
-   Define user journeys.
-   Define P0/P1/P2 scope.
-   Identify constraints.
-   Identify acceptance criteria.

Required output:

-   `docs/problem.md`
-   `docs/requirements.md`

No production coding should begin until the core P0 scope is clear.

------------------------------------------------------------------------

## Level 2 --- Architecture & Tool Selection

Goal:

-   Define system architecture.
-   Define modules.
-   Define database entities.
-   Define API boundaries.
-   Define authentication.
-   Define frontend information architecture.
-   Assign AI tools/tasks.

Required output:

-   `docs/architecture.md`
-   `docs/database.md`
-   API plan
-   task breakdown

Default architecture:

``` text
React + TypeScript + Vite
            |
          REST
            |
FastAPI + SQLAlchemy
            |
       PostgreSQL
```

------------------------------------------------------------------------

## Level 3 --- Implementation & Coding

Goal:

-   Implement vertical slices.
-   Keep frontend/backend/database integration working.
-   Build the inventory engine before adding cosmetic complexity.

Implementation order:

1.  Database foundation
2.  Inventory engine
3.  Authentication
4.  Products/categories
5.  Warehouses/locations
6.  Receipts
7.  Delivery orders
8.  Internal transfers
9.  Stock adjustments
10. Stock ledger/history
11. Dashboard
12. Search/filtering/alerts
13. UI polish
14. Optional enhancements

------------------------------------------------------------------------

## Level 4 --- Testing & Refinement

Goal:

-   Verify business logic.
-   Verify database consistency.
-   Verify API behavior.
-   Verify authorization.
-   Verify UI/UX.
-   Verify edge cases.
-   Verify stock invariants.

No feature is considered complete until its acceptance criteria and
relevant tests pass.

------------------------------------------------------------------------

## Level 5 --- Deployment & Limit Management

Goal:

-   Build production artifact.
-   Configure environment variables.
-   Apply migrations.
-   Deploy.
-   Smoke test.
-   Freeze the demo build.
-   Maintain AI-tool failover capability.

Final state:

``` text
Build -> Migration -> Deploy -> Smoke Test -> Demo Freeze -> Submission
```

------------------------------------------------------------------------

# 3. Event-Driven Development Cycle

Every major event produces an artifact.

  Event                   Artifact
  ----------------------- --------------------------------
  Problem received        `docs/problem.md`
  Requirements analyzed   `docs/requirements.md`
  Architecture approved   `docs/architecture.md`
  Database designed       `docs/database.md`
  Feature started         `.agents/tasks/TASK-XXX.md`
  Agent handoff           `.agents/handoffs/TASK-XXX.md`
  Feature complete        Tests + Git commit
  Integration complete    Integration report
  QA complete             Test report
  UI complete             UX checklist
  Deployment complete     Deployment record
  Demo freeze             `docs/demo.md`

------------------------------------------------------------------------

# 4. Problem Statement Intake Protocol

When a problem statement arrives:

## Step 1 --- Freeze coding

Do not immediately start coding.

## Step 2 --- Extract

Identify:

-   Target users
-   Business problem
-   Required workflows
-   Required entities
-   Required operations
-   Required statuses
-   Required dashboard information
-   Required filters
-   Additional features
-   Constraints
-   Missing/ambiguous requirements

## Step 3 --- Classify

### P0 --- Must work

Core business workflow.

### P1 --- Should work

Usability and operational improvements.

### P2 --- Nice to have

Optional differentiators.

## Step 4 --- Produce

``` text
Problem
Users
Pain points
Core workflows
Entities
Business rules
P0
P1
P2
Risks
Acceptance criteria
Demo scenario
```

------------------------------------------------------------------------

# 5. StockSense Functional Scope

## 5.1 Authentication

Required:

-   Sign up
-   Login
-   OTP-based password reset
-   Redirect authenticated users to Inventory Dashboard
-   Logout
-   Profile

Recommended roles:

-   `INVENTORY_MANAGER`
-   `WAREHOUSE_STAFF`

Role permissions must remain simple and directly connected to business
operations.

Do not create an unnecessarily complex authorization system.

------------------------------------------------------------------------

# 6. Authentication Design

## User table

``` text
users
-----
id
full_name
email
password_hash
role
is_active
created_at
updated_at
last_login_at
```

Constraints:

-   `email` unique
-   `password_hash` never returned through API
-   `role` constrained to supported roles
-   inactive users cannot authenticate

## Password reset

Use:

``` text
password_reset_otps
--------------------
id
user_id
otp_hash
expires_at
attempt_count
used_at
created_at
```

Rules:

-   OTP must expire.
-   OTP must be single-use.
-   Store a hashed OTP where practical.
-   Rate-limit reset requests.
-   Never log the OTP.
-   Never return OTP in API responses.
-   Do not store raw passwords.

------------------------------------------------------------------------

# 7. Product Database Schema

## products

``` text
products
--------
id
name
sku
category_id
uom_id
initial_stock
reorder_level
is_active
created_at
updated_at
```

Rules:

-   SKU must be unique.
-   Name required.
-   Category required.
-   Unit of measure required.
-   Initial stock cannot be negative.
-   Initial stock must not bypass ledger rules.

Recommended approach:

Initial stock creation should generate an initial stock transaction
rather than directly changing current stock.

------------------------------------------------------------------------

# 8. Product Categories

## categories

``` text
categories
----------
id
name
description
is_active
created_at
updated_at
```

Rules:

-   Category name should be unique within the expected scope.
-   Do not delete categories referenced by products; deactivate them
    instead.

------------------------------------------------------------------------

# 9. Units of Measure

## uoms

``` text
uoms
----
id
name
code
is_active
created_at
```

Examples:

``` text
kg
unit
piece
box
litre
```

The actual set should remain configurable.

------------------------------------------------------------------------

# 10. Warehouse and Location Model

The statement requires multi-warehouse support and location-aware stock.

## warehouses

``` text
warehouses
----------
id
name
code
address
is_active
created_at
updated_at
```

Rules:

-   Warehouse code unique.
-   Inactive warehouses cannot receive new operations.

## locations

``` text
locations
---------
id
warehouse_id
name
code
location_type
is_active
created_at
updated_at
```

Possible location types:

``` text
WAREHOUSE
RACK
PRODUCTION
STAGING
```

The system must support examples such as:

``` text
Main Warehouse -> Production Floor
Rack A -> Rack B
Warehouse 1 -> Warehouse 2
```

------------------------------------------------------------------------

# 11. Stock Balance

Current stock should be queryable by product and location.

Recommended table:

## stock_balances

``` text
stock_balances
--------------
id
product_id
location_id
quantity
updated_at
```

Unique constraint:

``` text
(product_id, location_id)
```

Rules:

-   Quantity must not become negative unless a future requirement
    explicitly permits negative stock.
-   Stock balance is a derived operational state maintained by the
    inventory service.
-   Every mutation must also create ledger records.
-   Direct UI modification of `stock_balances` is prohibited.

------------------------------------------------------------------------

# 12. Stock Ledger --- Core Audit Model

## stock_ledger

``` text
stock_ledger
------------
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

Rules:

1.  Every stock-changing operation creates ledger records.
2.  `quantity_after` must equal: `quantity_before + quantity_change`
3.  Ledger entries are append-only.
4.  Validated transactions must not be silently edited.
5.  Corrections should create compensating transactions.
6.  Every ledger record identifies the responsible user.
7.  Every ledger record references its source operation.

------------------------------------------------------------------------

# 13. Suppliers

The statement requires a supplier to be added to a receipt.

## suppliers

``` text
suppliers
---------
id
name
contact_name
email
phone
is_active
created_at
updated_at
```

Keep supplier management lightweight unless the problem statement later
requires a full procurement module.

------------------------------------------------------------------------

# 14. Customers

Delivery orders refer to customer shipment.

A lightweight customer entity is sufficient.

## customers

``` text
customers
---------
id
name
email
phone
address
is_active
created_at
updated_at
```

Do not build a full CRM.

------------------------------------------------------------------------

# 15. Receipts --- Incoming Stock

## receipts

``` text
receipts
--------
id
receipt_number
supplier_id
warehouse_id
destination_location_id
status
scheduled_at
created_by
validated_by
created_at
updated_at
validated_at
```

## receipt_items

``` text
receipt_items
-------------
id
receipt_id
product_id
quantity
uom_id
created_at
```

Workflow:

``` text
Create receipt
    ->
Add supplier
    ->
Add products
    ->
Enter quantities
    ->
Validate
    ->
Increase stock
    ->
Create ledger entries
    ->
Receipt becomes DONE
```

Example:

``` text
Receive 50 Steel Rods
Stock +50
```

------------------------------------------------------------------------

# 16. Delivery Orders --- Outgoing Stock

## deliveries

``` text
deliveries
----------
id
delivery_number
customer_id
warehouse_id
source_location_id
status
scheduled_at
created_by
validated_by
created_at
updated_at
validated_at
```

## delivery_items

``` text
delivery_items
--------------
id
delivery_id
product_id
quantity
uom_id
picked_quantity
packed_quantity
created_at
```

Workflow:

``` text
Create delivery
    ->
Pick
    ->
Pack
    ->
Validate
    ->
Check available stock
    ->
Decrease stock
    ->
Create ledger entries
    ->
Delivery becomes DONE
```

Rules:

-   Cannot validate more than available stock.
-   Quantity must be positive.
-   A canceled delivery must not change stock.
-   A validated delivery must not be validated again.

------------------------------------------------------------------------

# 17. Internal Transfers

## transfers

``` text
transfers
---------
id
transfer_number
warehouse_id
source_location_id
destination_location_id
status
scheduled_at
created_by
validated_by
created_at
updated_at
validated_at
```

## transfer_items

``` text
transfer_items
--------------
id
transfer_id
product_id
quantity
uom_id
created_at
```

Workflow:

``` text
Source location
      ->
Destination location
      ->
Product + quantity
      ->
Validate
      ->
Source stock -
Destination stock +
      ->
Ledger TRANSFER_OUT + TRANSFER_IN
```

Critical invariant:

``` text
Total stock before transfer == Total stock after transfer
```

Only location distribution changes.

------------------------------------------------------------------------

# 18. Inventory Adjustments

## adjustments

``` text
adjustments
-----------
id
adjustment_number
warehouse_id
location_id
status
reason
created_by
validated_by
created_at
updated_at
validated_at
```

## adjustment_items

``` text
adjustment_items
----------------
id
adjustment_id
product_id
system_quantity
counted_quantity
difference
created_at
```

Workflow:

``` text
Select product/location
      ->
Read recorded quantity
      ->
Enter physical count
      ->
Calculate difference
      ->
Validate
      ->
Update stock
      ->
Create adjustment ledger entry
```

Example:

``` text
Recorded = 100
Physical = 97
Difference = -3
New stock = 97
```

------------------------------------------------------------------------

# 19. Operation Status Model

The dashboard must support:

``` text
DRAFT
WAITING
READY
DONE
CANCELED
```

Recommended general transition:

``` text
DRAFT
  |
  v
WAITING
  |
  v
READY
  |
  v
DONE
```

Cancellation:

``` text
DRAFT / WAITING / READY
          |
          v
      CANCELED
```

Do not allow arbitrary status changes.

A validated `DONE` operation should be immutable except through a
controlled correction process.

------------------------------------------------------------------------

# 20. Database Relationships

Core relationships:

``` text
User
 |
 +---- Receipts
 +---- Deliveries
 +---- Transfers
 +---- Adjustments
 +---- Stock Ledger

Category
 |
 +---- Products

UOM
 |
 +---- Products
 +---- Receipt Items
 +---- Delivery Items
 +---- Transfer Items

Warehouse
 |
 +---- Locations
 +---- Receipts
 +---- Deliveries
 +---- Transfers
 +---- Adjustments

Location
 |
 +---- Stock Balances
 +---- Transfers
 +---- Adjustments
 +---- Stock Ledger

Product
 |
 +---- Stock Balances
 +---- Receipt Items
 +---- Delivery Items
 +---- Transfer Items
 +---- Adjustment Items
 +---- Stock Ledger
```

------------------------------------------------------------------------

# 21. Database Integrity Rules

The AI must verify:

## Uniqueness

``` text
users.email
products.sku
warehouses.code
locations.(warehouse_id, code)
receipts.receipt_number
deliveries.delivery_number
transfers.transfer_number
adjustments.adjustment_number
```

## Foreign keys

All references must use foreign keys.

## Quantity

For stock operations:

``` text
quantity > 0
```

For adjustment difference:

``` text
difference = counted_quantity - system_quantity
```

## Stock

Never directly mutate stock from a frontend route.

All stock changes go through:

``` text
Inventory Service
```

------------------------------------------------------------------------

# 22. Inventory Service Architecture

The central service should expose operations conceptually equivalent to:

``` text
receive_stock()
deliver_stock()
transfer_stock()
adjust_stock()
get_stock()
get_stock_by_location()
get_ledger()
```

Each operation must:

1.  Validate input.
2.  Validate business rules.
3.  Start a database transaction.
4.  Lock/read the relevant stock state safely.
5.  Update stock balance.
6.  Create ledger entry/entries.
7.  Mark the source document appropriately.
8.  Commit atomically.
9.  Return the resulting state.

On failure:

``` text
Rollback everything.
```

No partial inventory updates.

------------------------------------------------------------------------

# 23. Dashboard Requirements

Dashboard KPIs:

``` text
Total Products in Stock
Low Stock / Out of Stock Items
Pending Receipts
Pending Deliveries
Internal Transfers Scheduled
```

Filters:

``` text
Document Type
Status
Warehouse
Location
Product Category
```

Dashboard data must be dynamic.

Do not use permanent static JSON for production/demo data.

------------------------------------------------------------------------

# 24. Low Stock Rules

Each product may have:

``` text
reorder_level
```

Classification:

``` text
quantity == 0
    OUT_OF_STOCK

quantity <= reorder_level
    LOW_STOCK

quantity > reorder_level
    NORMAL
```

Dashboard should surface low-stock and out-of-stock items.

------------------------------------------------------------------------

# 25. API Architecture

Use REST endpoints with consistent naming.

## Auth

``` text
POST /api/auth/register
POST /api/auth/login
POST /api/auth/forgot-password
POST /api/auth/reset-password
GET  /api/auth/me
POST /api/auth/logout
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

## Warehouses / locations

``` text
GET  /api/warehouses
POST /api/warehouses
GET  /api/warehouses/{id}/locations
POST /api/warehouses/{id}/locations
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

------------------------------------------------------------------------

# 26. API Validation

Every request must use typed schemas.

Validate:

-   required fields
-   data types
-   quantity
-   IDs
-   status
-   authorization
-   business rules

Frontend validation is for UX.

Backend validation is authoritative.

------------------------------------------------------------------------

# 27. Frontend Architecture

Recommended:

``` text
frontend/
└── src/
    ├── components/
    ├── layouts/
    ├── pages/
    ├── features/
    │   ├── auth/
    │   ├── products/
    │   ├── receipts/
    │   ├── deliveries/
    │   ├── transfers/
    │   ├── adjustments/
    │   ├── dashboard/
    │   └── stock/
    ├── services/
    ├── hooks/
    ├── types/
    ├── utils/
    └── app/
```

------------------------------------------------------------------------

# 28. Navigation

Primary navigation:

``` text
Dashboard

Products

Operations
  Receipts
  Delivery Orders
  Inventory Adjustment
  Move History

Settings
  Warehouse

Profile
  My Profile
  Logout
```

This follows the supplied problem statement.

------------------------------------------------------------------------

# 29. UI/UX Standards

Every screen must have:

-   Clear visual hierarchy
-   Consistent spacing
-   Consistent typography
-   Consistent controls
-   Responsive layout
-   Loading states
-   Empty states
-   Error states
-   Success feedback
-   Disabled states
-   Confirmation for destructive actions
-   Search/filter where useful
-   Accessible labels
-   No broken navigation

Avoid:

-   unnecessary animations
-   excessive colors
-   dense unstructured tables
-   hidden actions
-   inconsistent buttons
-   long multi-step forms where a simpler flow is possible

------------------------------------------------------------------------

# 30. Core UI Screens

Minimum screens:

``` text
Login
Sign Up
Forgot Password
Reset Password

Dashboard

Products List
Product Create/Edit
Product Detail

Receipts List
Create Receipt
Receipt Detail

Delivery List
Create Delivery
Delivery Detail

Transfer List
Create Transfer
Transfer Detail

Adjustment List
Create Adjustment
Adjustment Detail

Move History

Warehouse Settings

Profile
```

------------------------------------------------------------------------

# 31. Search and Filters

Support:

``` text
SKU search
Product name search
Category filter
Warehouse filter
Location filter
Document type filter
Status filter
```

Filtering must query dynamic data rather than filtering only a small
hardcoded frontend dataset.

------------------------------------------------------------------------

# 32. Git Workflow

Branches:

``` text
main
develop
feature/*
fix/*
```

Feature example:

``` text
feature/receipt-workflow
feature/stock-ledger
feature/dashboard
feature/auth
```

Commit examples:

``` text
feat: add product creation API
feat: implement receipt validation
feat: add stock ledger
fix: prevent negative delivery stock
test: add transfer consistency tests
refactor: centralize inventory service
```

Never use:

``` text
final
final2
final-final
new-final
```

------------------------------------------------------------------------

# 33. AI Agent Roles

## Google Antigravity --- Orchestrator

Responsibilities:

-   Decompose work.
-   Assign tasks.
-   Track agent progress.
-   Coordinate parallel tasks.
-   Maintain task state.
-   Identify blocked tasks.
-   Prepare handoffs.

Antigravity must not independently redesign the architecture without
human approval.

------------------------------------------------------------------------

## Cursor --- Interactive Builder

Primary use:

-   React implementation
-   UI/UX
-   API integration
-   Rapid debugging
-   Small/medium feature implementation
-   Browser-facing work

Cursor must follow `.agents/rules/*`.

------------------------------------------------------------------------

## Codex --- Engineering Reviewer / Deep Implementation

Primary use:

-   Backend architecture
-   Database logic
-   Inventory service
-   Complex bugs
-   Tests
-   Refactoring
-   Security review
-   Code review
-   Transaction correctness

Codex must inspect existing code before modifying it.

------------------------------------------------------------------------

# 34. Agent Task Contract

Every task prompt must include:

``` text
CONTEXT
TASK
FILES
CONSTRAINTS
ACCEPTANCE CRITERIA
VERIFICATION
OUTPUT
```

Example:

``` text
CONTEXT:
StockSense inventory system.

TASK:
Implement receipt validation.

FILES:
backend/app/services/receipt_service.py
backend/app/models/
backend/app/schemas/

CONSTRAINTS:
Use existing SQLAlchemy models.
Do not change authentication.
Do not bypass inventory service.

ACCEPTANCE CRITERIA:
- Receipt can be validated once.
- Quantities must be positive.
- Stock increases correctly.
- Ledger entries are created.
- Transaction is atomic.
- Tests pass.

VERIFICATION:
Run receipt and inventory tests.

OUTPUT:
Summarize files changed, tests run, and unresolved issues.
```

------------------------------------------------------------------------

# 35. AI Handoff Protocol

When an agent reaches a limit, fails, or must switch:

1.  Stop after the current safe atomic operation.
2.  Save task state.
3.  Run tests if possible.
4.  Commit the working state.
5.  Create/update handoff file.
6.  Record remaining work.
7.  Select fallback tool.
8.  New agent reads project rules.
9.  New agent reads task state.
10. New agent inspects the current code.
11. New agent runs tests.
12. Continue from the checkpoint.

Never ask the replacement agent to rebuild the task from scratch.

------------------------------------------------------------------------

# 36. Task State Template

File:

`.agents/tasks/TASK-XXX.md`

``` markdown
# TASK-XXX

## Goal

## Requirement

## Current Level

## Owner

## Primary Agent

## Fallback Agent

## Status

NOT_STARTED / IN_PROGRESS / BLOCKED / COMPLETE

## Completed

-

## Remaining

-

## Files Changed

-

## Tests

-

## Known Issues

-

## Decisions

-

## Next Action

-

## Git Commit

-
```

------------------------------------------------------------------------

# 37. Handoff Template

File:

`.agents/handoffs/TASK-XXX.md`

``` markdown
# Handoff — TASK-XXX

## Previous Agent

## New Agent

## Current Status

## Completed Work

## Current Code State

## Tests Passed

## Tests Failed

## Known Issues

## Files Modified

## Important Decisions

## Do Not Change

## Exact Next Action

## Commit Hash
```

------------------------------------------------------------------------

# 38. Tool Limit Strategy

Use:

``` text
GREEN  = continue
YELLOW = prepare handoff
RED    = switch
```

Do not hard-code provider-specific usage numbers because quotas and
plans change.

The task state and Git repository are the durable source of truth.

Failover pattern:

``` text
Current Agent
     |
     v
Save State
     |
     v
Git Commit
     |
     v
Select Fallback
     |
     v
Read Rules
     |
     v
Read Task State
     |
     v
Run Tests
     |
     v
Continue
```

Default routing:

  Work                Primary       Fallback
  ------------------- ------------- ----------
  Orchestration       Antigravity   Human
  Frontend/UI         Cursor        Codex
  Backend             Codex         Cursor
  Database            Codex         Cursor
  Complex debugging   Codex         Cursor
  Parallel tasks      Antigravity   Cursor
  UI polish           Cursor        Codex
  Testing/review      Codex         Cursor

------------------------------------------------------------------------

# 39. Human Approval Gates

AI MUST request human approval before:

-   destructive database migration
-   deleting major modules
-   changing authentication
-   changing authorization
-   changing core stock logic
-   introducing a major dependency
-   changing architecture
-   exposing secrets
-   changing deployment configuration
-   modifying production data
-   changing core database constraints

------------------------------------------------------------------------

# 40. Testing Strategy

## Unit tests

Test:

-   stock calculations
-   quantity validation
-   status transitions
-   low-stock classification
-   authentication logic
-   permission checks

## Integration tests

Test:

``` text
Receipt -> Stock -> Ledger
Delivery -> Stock -> Ledger
Transfer -> Location Stock -> Ledger
Adjustment -> Stock -> Ledger
```

## API tests

Test:

-   success responses
-   validation errors
-   unauthorized requests
-   forbidden requests
-   missing resources
-   duplicate operations

## UI tests

Test:

-   navigation
-   form validation
-   loading
-   error states
-   successful workflows
-   filters
-   responsive behavior

------------------------------------------------------------------------

# 41. Inventory Invariants

These are mandatory.

## Receipt

``` text
stock_after = stock_before + received_quantity
```

## Delivery

``` text
stock_after = stock_before - delivered_quantity
```

and:

``` text
delivered_quantity <= available_quantity
```

## Transfer

``` text
source_after = source_before - quantity
destination_after = destination_before + quantity
```

and:

``` text
total_stock_before == total_stock_after
```

## Adjustment

``` text
difference = counted_quantity - system_quantity
new_quantity = counted_quantity
```

## Ledger

``` text
quantity_after =
quantity_before + quantity_change
```

------------------------------------------------------------------------

# 42. Database Transaction Rules

All stock-changing operations must execute atomically.

Pseudo-flow:

``` text
BEGIN TRANSACTION

Validate source document

Read/lock relevant stock

Check business rules

Update stock balance

Create ledger entry

Update operation status

COMMIT
```

On any failure:

``` text
ROLLBACK
```

No partial stock update is acceptable.

------------------------------------------------------------------------

# 43. Security Requirements

Minimum:

-   Hash passwords.
-   Never store plaintext passwords.
-   Never commit `.env`.
-   Use environment variables for secrets.
-   Validate authorization on backend.
-   Protect authenticated routes.
-   Validate all user input.
-   Avoid SQL injection through ORM/query parameters.
-   Avoid exposing internal errors to clients.
-   Rate-limit OTP/password reset operations.
-   Do not log passwords, OTPs, tokens, or secrets.

------------------------------------------------------------------------

# 44. Environment Variables

Use:

`.env.example`

Example:

``` env
DATABASE_URL=
JWT_SECRET=
OTP_SECRET=
CORS_ORIGINS=
```

Never commit:

``` text
.env
```

The frontend must not contain server secrets.

------------------------------------------------------------------------

# 45. Local Development

Recommended backend:

``` bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Run FastAPI using the project's configured command.

Recommended frontend:

``` bash
npm install
npm run dev
```

Database:

``` text
PostgreSQL 18
localhost:5432
```

------------------------------------------------------------------------

# 46. Database Migration

Use Alembic with SQLAlchemy.

Rules:

1.  Schema changes must be migrations.
2.  Do not manually alter production schema.
3.  Review generated migrations.
4.  Test migrations locally.
5.  Never delete production data during a normal migration.
6.  Database migration must be reviewed before merge.

------------------------------------------------------------------------

# 47. Seed Data

Create development seed data for:

``` text
Users
Categories
UOMs
Warehouses
Locations
Products
Suppliers
Customers
```

Include realistic inventory examples:

``` text
Steel Rods
Chairs
Bolts
Finished Frames
```

Seed data is for development/demo only and must not replace dynamic
application behavior.

------------------------------------------------------------------------

# 48. Demo Scenario

The primary demo should tell one complete inventory story.

``` text
1. Login
2. Dashboard
3. Show current stock
4. Receive 100 kg Steel
5. Validate receipt
6. Show stock +100
7. Transfer 20 kg to Production Rack
8. Show location distribution
9. Deliver 20 kg
10. Show stock decrease
11. Record 3 kg damaged
12. Validate adjustment
13. Open Stock Ledger
14. Show complete audit trail
15. Show low-stock/dashboard effect
```

This follows the supplied problem statement's simplified inventory flow.

------------------------------------------------------------------------

# 49. Demo Freeze

Once the complete demo works:

-   Stop major feature development.
-   Create a Git checkpoint.
-   Run all critical tests.
-   Verify database.
-   Verify environment variables.
-   Verify deployment.
-   Verify demo credentials.
-   Verify the demo workflow from a clean browser session.

No risky feature additions after demo freeze.

------------------------------------------------------------------------

# 50. P0/P1/P2 Feature Policy

## P0

Must be complete before P1.

``` text
Authentication
Products
Warehouse/location
Receipts
Deliveries
Transfers
Adjustments
Stock ledger
Dashboard
```

## P1

Only after P0:

``` text
Search
Filters
Low-stock alerts
Move history
Role permissions
Multi-warehouse refinement
Responsive polish
```

## P2

Only if P0 and P1 are stable:

``` text
Advanced analytics
Barcode
AI assistance
Predictive reorder
Advanced notifications
CSV import/export
```

------------------------------------------------------------------------

# 51. Definition of Done

A feature is DONE only when:

``` text
[ ] Requirement identified
[ ] API implemented
[ ] Database behavior verified
[ ] Input validation implemented
[ ] Authorization checked
[ ] Business rules implemented
[ ] Error handling implemented
[ ] UI integrated
[ ] Loading state implemented
[ ] Empty state implemented
[ ] Error state implemented
[ ] Tests pass
[ ] No unrelated regressions
[ ] Git commit created
[ ] Task state updated
```

------------------------------------------------------------------------

# 52. AI Review Checklist

Before an agent declares a feature complete, ask:

``` text
What requirement does this implement?

What files changed?

What business rules were enforced?

What database changes were made?

What tests were added?

What tests were executed?

What edge cases were considered?

What assumptions were made?

Are there known issues?

Can another agent continue from the current state?
```

------------------------------------------------------------------------

# 53. Final Architecture

``` text
                         HUMAN TEAM
                              |
                              v
                       ANTIGRAVITY
                       ORCHESTRATOR
                              |
              +---------------+---------------+
              |               |               |
              v               v               v
           CURSOR           CODEX           HUMAN
           BUILD            REVIEW          DECIDE
              |               |               |
              +---------------+---------------+
                              |
                              v
                           GITHUB
                              |
                              v
                       TEST / VALIDATE
                              |
                              v
                           DEPLOY
                              |
                              v
                            DEMO
```

Tool responsibilities:

``` text
Antigravity = orchestrate
Cursor      = implement/interact
Codex       = reason/review/test
Human       = approve decisions
Git         = persistent state
PostgreSQL  = source of inventory data
Ledger      = source of stock history
```

------------------------------------------------------------------------

# 54. Final Execution Sequence

When the hackathon starts:

``` text
01. Read problem statement
02. Freeze coding
03. Create problem brief
04. Extract requirements
05. Define P0/P1/P2
06. Define user journeys
07. Design architecture
08. Design database
09. Review schema
10. Create tasks
11. Assign agents
12. Implement database foundation
13. Implement inventory engine
14. Implement authentication
15. Implement products
16. Implement receipts
17. Implement deliveries
18. Implement transfers
19. Implement adjustments
20. Implement ledger/history
21. Implement dashboard
22. Add search/filter/alerts
23. Polish UI/UX
24. Run tests
25. Run security review
26. Deploy
27. Smoke test
28. Freeze demo
29. Run complete demo scenario
30. Submit
```

------------------------------------------------------------------------

# 55. Absolute Rules

1.  **P0 before P1.**
2.  **P1 before P2.**
3.  **No AI-generated code without verification.**
4.  **No direct stock mutation outside the inventory service.**
5.  **Every stock mutation creates a ledger record.**
6.  **Validated operations are immutable.**
7.  **Database changes require migrations.**
8.  **Secrets never enter Git.**
9.  **Every agent reads this workflow before working.**
10. **Every handoff includes task state.**
11. **Every major feature gets a Git checkpoint.**
12. **Human approval is required for architecture/security/destructive
    changes.**
13. **The demo must use dynamic application data.**
14. **The UI must remain responsive and usable.**
15. **Never sacrifice a working P0 feature for an unfinished WOW
    feature.**
16. **When an AI tool reaches its limit, preserve state and fail over;
    never restart the task blindly.**
17. **The repository is the shared source of implementation truth.**
18. **The database is the source of current inventory state.**
19. **The stock ledger is the source of inventory history.**
20. **When uncertain, stop, document the uncertainty, and request human
    confirmation.**

------------------------------------------------------------------------

# 56. Current Project Status

At project initialization:

``` text
Level 1 — Concept & Scope       READY/COMPLETE
Level 2 — Architecture          READY
Level 2 — Database Design       NEXT
Level 3 — Implementation        NOT STARTED
Level 4 — Testing               NOT STARTED
Level 5 — Deployment            NOT STARTED
```

Immediate next tasks:

``` text
TASK-001
Finalize PostgreSQL schema

TASK-002
Create SQLAlchemy models

TASK-003
Create Alembic migration

TASK-004
Create FastAPI application skeleton

TASK-005
Implement authentication

TASK-006
Implement inventory service

TASK-007
Implement stock ledger
```

**Do not begin frontend-heavy development until the database and
inventory transaction model have been reviewed.**

------------------------------------------------------------------------

# 57. Source Alignment

The functional requirements in this workflow are derived from the
supplied StockSense problem statement, including:

-   centralized real-time inventory management
-   Inventory Manager and Warehouse Staff users
-   authentication and OTP reset
-   dashboard KPIs and dynamic filters
-   product management
-   receipts
-   delivery orders
-   internal transfers
-   stock adjustments
-   move history
-   warehouses
-   low-stock alerts
-   multi-warehouse support
-   SKU search and smart filters
-   stock-ledger-based inventory flow

The problem statement is the authoritative source for competition
requirements. Where this workflow proposes implementation details that
the statement does not explicitly define---such as exact database
tables, API routes, technology choices, role permissions, or
transaction-locking strategy---those are engineering decisions for
implementing the stated requirements and must not be represented as
official competition requirements.

------------------------------------------------------------------------

# END OF WORKFLOW
