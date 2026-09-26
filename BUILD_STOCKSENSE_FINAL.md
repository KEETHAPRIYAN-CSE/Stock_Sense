# StockSense — Current-Codebase Build & Completion Specification

> **This is the master instruction for the coding agent.**
>
> StockSense is NOT a greenfield project anymore. The existing repository already contains substantial backend, frontend, database, authentication, OTP, authorization, inventory, API, and testing work.
>
> **Do not rebuild the project from scratch. Inspect the existing implementation first, preserve working code, fix broken functionality, implement missing functions, then polish the frontend.**

---

# 0. CURRENT PROJECT STATE

The current project analysis reports that:

- Core architecture and database design exist.
- Product/category/UOM/warehouse/location/supplier/customer models exist.
- Receipt, delivery, transfer, and adjustment models exist.
- FastAPI backend exists.
- JWT authentication and bcrypt password hashing exist.
- OTP password-reset service exists.
- Inventory transactions use row-level locking.
- API routers exist.
- React + Vite frontend exists.
- Backend tests exist.
- Production frontend build is configured.
- Docker is NOT required.

However, the current implementation has critical authentication gaps:

1. Sign-up does not reliably create a persistent user account.
2. OTP password reset is not reliably working.
3. Authentication must be verified against the same database used by signup.
4. Authorization must be verified at the backend endpoint level.
5. Several UI and business functions shown in the StockSense wireframes are still missing.
6. Frontend needs visual and interaction polish.
7. Pagination/export/RBAC and other secondary functions may still be incomplete.

Therefore:

## AUTHENTICATION IS A P0 BLOCKER.

Do not consider authentication complete until the complete registration → login → forgot password → OTP → reset password → login flow works against the real database.

---

# 1. PRIMARY OBJECTIVE

Bring the existing StockSense application to a complete hackathon-ready state.

The agent must:

```text
INSPECT EXISTING CODE
        ↓
BASELINE TESTS
        ↓
FIX DATABASE/AUTHENTICATION
        ↓
VERIFY AUTHORIZATION
        ↓
AUDIT MISSING FEATURES
        ↓
IMPLEMENT P0 BUSINESS FUNCTIONS
        ↓
IMPLEMENT MISSING UI FUNCTIONS
        ↓
POLISH FRONTEND
        ↓
IMPLEMENT P1 FUNCTIONS
        ↓
RUN END-TO-END TESTS
        ↓
RUN DEMO FLOW
        ↓
FINAL CODE REVIEW
```

Do not blindly generate duplicate files.

Do not replace working modules without a reason.

---

# 2. NON-NEGOTIABLE RULES

## 2.1 Inspect first

Before modifying anything:

1. Inspect repository structure.
2. Inspect `README.md`.
3. Inspect environment configuration.
4. Inspect database configuration.
5. Inspect user model.
6. Inspect authentication routes/services.
7. Inspect OTP implementation.
8. Inspect authorization dependencies.
9. Inspect frontend authentication flow.
10. Inspect existing tests.
11. Run the existing test suite.
12. Run the existing frontend build.

Create:

```text
.agents/tasks/000-codebase-audit.md
```

containing the actual current state.

---

## 2.2 Preserve working code

Do NOT:

- recreate the project,
- delete working authentication code,
- replace the frontend framework,
- replace FastAPI,
- replace PostgreSQL,
- replace the database architecture,
- remove existing tests,
- introduce microservices.

Modify existing code when appropriate.

---

# 3. TECHNOLOGY REQUIREMENTS

Use the existing stack.

## Backend

- Python
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Pydantic
- JWT
- bcrypt-compatible password hashing
- pytest

## Frontend

- React
- TypeScript
- Vite
- React Router
- Axios or existing API client

## Database

PostgreSQL is the authoritative database for normal development.

SQLite fallback may remain only if already implemented and safe, but it must NEVER cause different authentication/inventory state between requests.

---

# 4. DO NOT USE DOCKER

Docker is explicitly NOT required.

Do not spend implementation time on:

```text
Dockerfile
docker-compose
container orchestration
Kubernetes
```

The application must run using the local development environment.

Expected architecture:

```text
React/Vite
    ↓
FastAPI
    ↓
SQLAlchemy
    ↓
PostgreSQL
```

---

# 5. DATABASE CONSISTENCY — P0

This is a critical requirement.

The same configured database must be used by:

- signup,
- login,
- current-user,
- logout/session validation,
- forgot password,
- OTP verification,
- password reset,
- authorization,
- products,
- warehouses,
- locations,
- receipts,
- deliveries,
- transfers,
- adjustments,
- stock balances,
- stock ledger,
- dashboard.

Never allow this situation:

```text
Signup → PostgreSQL
Login → SQLite
```

or:

```text
Signup → SQLite
Forgot Password → PostgreSQL
```

Inspect:

- `DATABASE_URL`
- SQLAlchemy engine creation
- session dependency
- initialization code
- fallback logic
- test database configuration

Ensure database selection is deterministic.

Add a health/database diagnostic endpoint or internal diagnostic where useful.

---

# 6. AUTHENTICATION — P0 BLOCKER

Authentication is not complete until all of the following pass.

---

## 6.1 User schema

Verify the user table contains appropriate fields:

```text
id
login_id
full_name
email
password_hash
role
is_active
created_at
updated_at
last_login_at
```

Required:

```text
login_id UNIQUE
email UNIQUE
```

Passwords must NEVER be stored as plaintext.

---

# 7. SIGNUP — MUST ACTUALLY CREATE AN ACCOUNT

Implement and verify:

```text
Signup form
    ↓
Frontend validation
    ↓
POST /api/auth/register
    ↓
Backend validation
    ↓
Check duplicate login_id
    ↓
Check duplicate email
    ↓
Validate password
    ↓
Hash password
    ↓
INSERT user
    ↓
COMMIT transaction
    ↓
Return created-user response
    ↓
Frontend redirects to Login
```

After registration, verify directly through the database or authenticated API that the user exists.

### Login ID rules

From the provided wireframe:

- Must be unique.
- Must be 6–12 characters.

### Password rules

Implement the application's intended password rules consistently in both frontend and backend.

At minimum enforce the specified complexity:

- lowercase
- uppercase
- numeric/special requirements as defined by the existing project
- minimum length greater than 8 where specified

Never rely only on frontend validation.

---

# 8. LOGIN — P0

Login must work using an account created through the signup form.

Test:

```text
Create account
    ↓
Logout/return to login
    ↓
Login with newly created credentials
    ↓
Verify password
    ↓
Verify active user
    ↓
Generate JWT
    ↓
Store/use authentication state
    ↓
Open dashboard
```

Test invalid credentials.

Test disabled account.

Test expired/invalid token.

Test protected endpoint without token.

---

# 9. AUTHORIZATION — P0

Authentication answers:

```text
Who are you?
```

Authorization answers:

```text
What are you allowed to do?
```

Enforce authorization on the backend.

Roles:

```text
INVENTORY_MANAGER
WAREHOUSE_STAFF
```

At minimum audit access to:

- products,
- categories,
- warehouses,
- locations,
- suppliers,
- customers,
- receipts,
- deliveries,
- transfers,
- adjustments,
- stock,
- dashboard.

Do not rely only on hiding buttons in React.

---

# 10. FORGOT PASSWORD / OTP — P0

The OTP system must actually work.

---

## 10.1 Request OTP

Flow:

```text
Forgot Password
      ↓
Enter email/login ID
      ↓
Find user
      ↓
Generate cryptographically secure OTP
      ↓
Hash OTP
      ↓
Store OTP hash
      ↓
Set expiration
      ↓
Set attempt counter
      ↓
Invalidate older active OTPs
      ↓
Return development-safe OTP response if email delivery is not configured
```

For hackathon development, SMTP is NOT mandatory.

It is acceptable to expose the OTP in development mode only, but:

- clearly mark it as development mode,
- never log it as a secret in production,
- still store the hashed OTP,
- still verify it against the database.

---

# 11. OTP DATABASE REQUIREMENTS

Verify a table similar to:

```text
password_reset_otps
-------------------
id
user_id
otp_hash
expires_at
attempt_count
used_at
created_at
```

Requirements:

- OTP hash stored, not plaintext.
- OTP expiration enforced.
- OTP attempt limit enforced.
- Used OTP cannot be reused.
- Old active OTPs invalidated when a new one is created.
- OTP belongs to the correct user.

---

# 12. OTP VERIFICATION

Flow:

```text
User enters OTP
      ↓
Find active OTP
      ↓
Check user
      ↓
Check expiration
      ↓
Check attempt limit
      ↓
Verify hash
      ↓
Mark OTP as verified/used
      ↓
Allow password reset
```

Test:

- Correct OTP
- Wrong OTP
- Expired OTP
- Used OTP
- Too many attempts
- OTP belonging to another user

---

# 13. PASSWORD RESET

Flow:

```text
Valid OTP
   ↓
New password
   ↓
Confirm password
   ↓
Validate password
   ↓
Hash password
   ↓
UPDATE users.password_hash
   ↓
Invalidate OTP
   ↓
COMMIT
   ↓
Return success
```

Then test:

```text
Old password → rejected
New password → accepted
```

This is mandatory.

---

# 14. AUTHENTICATION ACCEPTANCE TEST

The following must pass:

```text
1. Open Signup
2. Create a completely new user
3. Confirm no duplicate error
4. Confirm account exists in database
5. Go to Login
6. Login with new account
7. Open Dashboard
8. Logout
9. Open Forgot Password
10. Request OTP
11. Receive development OTP
12. Enter OTP
13. Enter new password
14. Reset password
15. Login with new password
16. Verify protected pages
17. Verify unauthorized operations are rejected
```

Do not declare authentication complete until this entire sequence passes.

---

# 15. EXISTING DATABASE MODEL

Preserve and verify the existing inventory schema.

Core entities:

```text
users
password_reset_otps

categories
uoms
products

warehouses
locations

suppliers
customers

stock_balances
stock_ledger

receipts
receipt_items

deliveries
delivery_items

transfers
transfer_items

adjustments
adjustment_items

reorder_rules
```

---

# 16. INVENTORY ENGINE — DO NOT BREAK

Existing inventory logic uses transaction safety and row-level locking.

Preserve this behavior.

Stock-changing functions should remain centralized:

```python
receive_stock()
deliver_stock()
transfer_stock()
adjust_stock()
get_stock()
get_stock_by_location()
get_ledger()
```

Do not duplicate stock calculations inside React.

---

# 17. INVENTORY INVARIANTS

## Receipt

```text
after = before + received
```

## Delivery

```text
after = before - delivered
```

Never:

```text
delivered > available
```

## Transfer

```text
source_after = source_before - quantity
destination_after = destination_before + quantity
```

Total stock remains unchanged.

## Adjustment

```text
difference = counted - system
new_quantity = counted
```

## Ledger

```text
quantity_after = quantity_before + quantity_change
```

---

# 18. MISSING FUNCTION AUDIT — P0

After fixing authentication, inspect the entire current implementation and compare it with this specification.

For every feature:

```text
UI exists?
API exists?
Schema exists?
Service exists?
Database operation works?
Frontend connected?
Error state works?
Loading state works?
Tests exist?
```

Create:

```text
.agents/tasks/missing-functions.md
```

with:

```text
Feature
Current status
Missing layer
Required change
Priority
Test
```

Do not assume a feature is complete just because a button exists.

---

# 19. STOCK PAGE — P0

Create/complete the stock view shown in the wireframes.

Columns:

```text
Product
Per Unit Cost
On Hand
Reserved
Free to Use
```

Formula:

```text
Free to Use = On Hand - Reserved
```

The values must come from the backend.

Do not hard-code them.

Allow:

- product search,
- filters,
- location/warehouse filtering,
- stock details,
- appropriate stock actions.

---

# 20. RESERVED STOCK

Support the concept:

```text
On Hand
Reserved
Free to Use
```

At minimum, calculate:

```text
free_to_use = on_hand - reserved
```

Do not allow free-to-use stock to become negative unless the business rules explicitly allow it.

If reservation logic is not yet fully modeled, implement the smallest correct backend representation required by the current application rather than faking it in the UI.

---

# 21. WAREHOUSE MANAGEMENT — P0

Warehouse form:

```text
Name
Short Code
Address
```

Required:

- Create
- Read
- Update
- List
- Search
- Validation
- Unique short code

---

# 22. LOCATION MANAGEMENT — P0

Location form:

```text
Name
Short Code
Warehouse
```

A location belongs to a warehouse.

Constraint:

```text
UNIQUE(warehouse_id, code)
```

Support:

- Create
- Read
- Update
- List
- Search
- Warehouse filtering

---

# 23. RECEIPTS — P0

Wireframe behavior:

- Click Operations → Receipts.
- Default to List View.
- Search.
- Switch List/Kanban.
- Create new receipt.

Reference format:

```text
WH/IN/0001
```

Receipt list fields:

```text
Reference
Date
From / Vendor
To
Contact
Schedule Date
Status
```

Receipt detail:

```text
Reference
Receive From
Schedule Date
Responsible
Operation Type
Products
Quantity
```

Actions:

```text
Validate
Print
Cancel
```

Status flow:

```text
Draft → Ready → Done
```

If the existing system uses:

```text
Draft → Waiting → Ready → Done
```

preserve the existing valid state machine and use the wireframe terminology consistently in the UI.

---

# 24. RECEIPT BEHAVIOR

On validation:

```text
Receipt
  ↓
Increase destination stock
  ↓
Create ledger entry
  ↓
Mark DONE
```

Responsible user should default to the currently logged-in user where appropriate.

---

# 25. DELIVERY — P0

Delivery list:

```text
Reference
From
To
Contact
Schedule Date
Status
```

Reference:

```text
WH/OUT/0001
```

Actions:

```text
Validate
Print
Cancel
```

Workflow:

```text
Draft
↓
Waiting
↓
Ready
↓
Done
```

Delivery must verify stock before completion.

If stock is insufficient:

```text
Reject transaction
Explain the problem clearly
Do not partially update stock
Do not create an incorrect ledger entry
```

---

# 26. DELIVERY UI STATUS

The wireframes describe:

```text
Draft = initial state
Waiting = waiting for required stock
Ready = ready to deliver/receive
Done = completed
```

Also support late status when appropriate.

---

# 27. LATE OPERATIONS

An operation is late when:

```text
schedule_date < today
```

and it is not completed/canceled.

The dashboard should identify late operations.

Do not permanently store "late" if it can be derived safely from schedule date and status.

---

# 28. WAITING OPERATIONS

An operation is waiting when it is waiting for required stock or another prerequisite.

The backend should determine this where possible.

Do not fake waiting status in React.

---

# 29. MOVE HISTORY — P0

Create/complete Move History.

Columns:

```text
Reference
Date
Contact
From
To
Quantity
Status
```

Support:

- search by reference,
- search by contact,
- date filtering,
- status filtering,
- list view,
- Kanban view.

If one reference contains multiple products, display the products correctly.

Each stock movement should be traceable to its source operation.

---

# 30. LIST / KANBAN VIEW SWITCHING

Implement view switching for applicable operations:

```text
List
Kanban
```

The view toggle must not reload or lose filter state unnecessarily.

Kanban should group operations by meaningful status.

---

# 31. SEARCH AND FILTERING

Implement real backend/API filtering where datasets can become large.

At minimum support:

Products:

```text
name
SKU
category
warehouse/location
```

Receipts:

```text
reference
supplier/contact
status
date
```

Deliveries:

```text
reference
customer/contact
status
date
```

Move History:

```text
reference
contact
status
date
```

---

# 32. PAGINATION — P1

The current system may return every record.

Implement backend pagination for major list APIs.

Use a consistent model such as:

```text
page
page_size
total
items
```

or the project's existing equivalent.

Frontend must display:

- current page,
- total pages/records where available,
- next,
- previous.

Do not break existing API consumers.

---

# 33. CSV EXPORT — P1

Implement CSV export for useful inventory lists.

At minimum consider:

- Products
- Stock
- Move History
- Receipts
- Deliveries

Export current filters when practical.

Do not generate fake exports.

---

# 34. PRINT — P1

Implement print-friendly views for:

- Receipt
- Delivery
- Transfer where appropriate

Print should show:

```text
Reference
Date
Warehouse
Locations
Responsible
Products
Quantities
Status
```

Use browser print functionality or a clean printable route.

---

# 35. DASHBOARD — P0

Dashboard should show operational statistics.

Required:

```text
Receipts
Deliveries
```

For example:

```text
Receipt
4 to receive
1 late
6 operations
```

```text
Delivery
4 to deliver
1 late
2 waiting
6 operations
```

Values must come from APIs.

Do not hard-code.

---

# 36. DASHBOARD FILTERS

Support appropriate filters:

```text
Document Type
Status
Warehouse
Location
Product Category
Date
```

The dashboard should update from backend query results.

---

# 37. PRODUCT MANAGEMENT — P0

Support:

- Create product
- Update product
- List product
- Search product
- SKU uniqueness
- Category
- UOM
- Initial stock
- Reorder level
- Active/inactive
- Stock by location
- Per-unit cost if present in the existing schema/business model

---

# 38. PRODUCT CREATION FROM OPERATION

If the wireframe allows adding a new product while creating an operation:

```text
Add New Product
```

implement a proper modal/form.

After successful creation:

```text
new product becomes selectable
```

Do not require a full page reload.

---

# 39. MASTER DATA

Complete:

```text
Categories
UOM
Warehouses
Locations
Suppliers
Customers
```

Each must have:

- proper API,
- database persistence,
- validation,
- UI,
- error handling.

---

# 40. FRONTEND POLISH — P1

The wireframes use a dark interface with a coral/pink visual accent.

Create a polished, professional inventory UI inspired by the wireframes without blindly copying the hand-drawn appearance.

Use:

- dark background,
- clear cards,
- readable typography,
- consistent accent color,
- subtle borders,
- clear status badges,
- professional tables,
- consistent spacing,
- responsive layout.

Avoid:

- excessive animations,
- excessive gradients,
- unreadable neon text,
- decorative clutter,
- inconsistent button styles.

---

# 41. NAVIGATION

Required main navigation:

```text
Dashboard
Operations
Products
Stock
Move History
Settings
```

Settings should contain:

```text
Warehouses
Locations
```

Profile area:

```text
My Profile
Logout
```

---

# 42. LOADING / EMPTY / ERROR STATES

Every API-backed page must handle:

### Loading

Show a useful loading state.

### Empty

Explain that no records currently exist.

### Error

Show a user-friendly message.

### Success

Show confirmation after successful operations.

Never leave the screen blank.

---

# 43. FORM VALIDATION

Validate both frontend and backend.

Forms must clearly indicate:

- required fields,
- invalid values,
- duplicate identifiers,
- password errors,
- insufficient stock,
- invalid quantities.

Do not rely only on browser validation.

---

# 44. AUTHENTICATED USER EXPERIENCE

After login:

```text
Login
 ↓
Dashboard
```

The UI should display the current user's identity where appropriate.

Operation forms should automatically populate:

```text
Responsible
Created By
```

using the authenticated user.

---

# 45. SECURITY

Verify:

- Password hashing
- JWT validation
- Protected endpoints
- Backend RBAC
- Input validation
- SQL injection protection
- OTP expiration
- OTP attempt limits
- Secure errors
- CORS
- Environment secrets
- No plaintext passwords
- No production OTP logging

Never expose database credentials.

---

# 46. TESTING

Do not remove existing tests.

Add/fix tests for:

## Authentication

- Registration creates database user
- Duplicate login ID
- Duplicate email
- Login
- Invalid password
- Disabled user
- JWT
- Logout/session behavior

## OTP

- OTP generated
- OTP stored as hash
- Correct OTP
- Incorrect OTP
- Expired OTP
- Used OTP
- Attempt limit
- Password reset

## Authorization

- Manager permissions
- Warehouse staff permissions
- Unauthorized endpoint access

## Inventory

- Receipt
- Delivery
- Transfer
- Adjustment
- Ledger
- Concurrency
- Negative stock prevention

## Frontend/API integration

- Authenticated requests
- Protected route behavior
- Operation validation
- Error handling

---

# 47. MANDATORY AUTH E2E TEST

Automate where practical:

```text
CREATE USER
   ↓
READ USER FROM DB
   ↓
LOGIN
   ↓
GET /auth/me
   ↓
REQUEST OTP
   ↓
VERIFY OTP
   ↓
RESET PASSWORD
   ↓
LOGIN WITH NEW PASSWORD
```

This is a release-blocking test.

---

# 48. INVENTORY E2E TEST

Run:

```text
Login
↓
Receive 100 kg Steel
↓
Validate
↓
Stock +100
↓
Transfer 20 kg
↓
Source -20
↓
Destination +20
↓
Total unchanged
↓
Deliver 20 kg
↓
Stock -20
↓
Adjust -3 kg damaged
↓
Final stock correct
↓
Ledger contains all movements
↓
Refresh page
↓
Data still correct
```

---

# 49. DEMO DATA

Use realistic demo data.

Example products:

```text
Steel Rods
Chairs
Bolts
Finished Frames
```

Example locations:

```text
Main Store
Production Rack
Rack A
Rack B
```

Demo seed data must be stored through the database.

Do not hard-code demo data into React.

---

# 50. REFERENCE NUMBERING

Implement deterministic document references.

Examples:

```text
WH/IN/0001
WH/IN/0002

WH/OUT/0001
WH/OUT/0002

WH/INT/0001

WH/ADJ/0001
```

Reference IDs must be unique.

Do not generate references solely in the frontend.

---

# 51. FILE STRUCTURE

Preserve the existing repository structure where possible.

Expected high-level structure:

```text
StockSense/
│
├── README.md
├── WORKFLOW.md
├── BUILD_STOCKSENSE.md
├── .gitignore
├── .env.example
│
├── .agents/
│   ├── rules/
│   ├── prompts/
│   ├── tasks/
│   └── handoffs/
│
├── docs/
│
├── backend/
│   ├── app/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── repositories/
│   │   ├── services/
│   │   ├── api/
│   │   └── utils/
│   ├── alembic/
│   └── tests/
│
├── frontend/
│   └── src/
│
└── scripts/
```

Do not create Docker files as part of this specification.

---

# 52. AGENT TASK FILES

Create/update:

```text
.agents/tasks/000-codebase-audit.md
.agents/tasks/001-authentication-fix.md
.agents/tasks/002-authorization-audit.md
.agents/tasks/003-missing-backend-functions.md
.agents/tasks/004-missing-frontend-functions.md
.agents/tasks/005-stock-page.md
.agents/tasks/006-receipts.md
.agents/tasks/007-deliveries.md
.agents/tasks/008-move-history.md
.agents/tasks/009-dashboard.md
.agents/tasks/010-ui-polish.md
.agents/tasks/011-pagination-export.md
.agents/tasks/012-e2e-testing.md
.agents/tasks/013-final-review.md
```

Each task must include:

```markdown
# Objective

# Current State

# Files

# Required Changes

# Acceptance Criteria

# Verification

# Status
```

---

# 53. WORKING METHOD

For every task:

```text
1. Read task
2. Inspect current implementation
3. Identify missing pieces
4. Implement
5. Run relevant tests
6. Fix failures
7. Re-run tests
8. Update task status
9. Continue
```

Never mark a task complete because code was written.

Mark it complete only after verification.

---

# 54. PRIORITY SYSTEM

## P0 — Must work

```text
Authentication
Signup persistence
Login
OTP
Password reset
Authorization
Database consistency

Products
Warehouses
Locations

Receipts
Deliveries
Transfers
Adjustments

Stock
Stock Ledger

Dashboard

Search
Core filtering

E2E inventory flow
```

## P1 — Important

```text
Pagination
CSV export
Print
List/Kanban
Advanced filtering
UI polish
Better empty/loading/error states
Granular RBAC
```

## P2 — Optional

```text
Advanced analytics
Barcode support
Predictive reorder
Advanced notifications
AI assistance
```

Do not implement P2 before P0 is stable.

---

# 55. DO NOT ADD UNNECESSARY TECHNOLOGY

Do not introduce:

```text
Microservices
Kafka
Kubernetes
Blockchain
RAG
LLM
Redis
Celery
Docker
```

unless there is a demonstrated requirement.

The hackathon value comes from a complete, working inventory system.

---

# 56. DATABASE MIGRATIONS

Use Alembic for schema changes.

Before changing schema:

1. Inspect current migration history.
2. Create a new migration.
3. Apply migration locally.
4. Run tests.
5. Verify existing data is preserved.

Never casually delete the database.

Never run destructive reset commands without human approval.

---

# 57. API CONTRACT

Do not break existing API consumers unnecessarily.

Before changing an endpoint:

- inspect frontend usage,
- inspect backend tests,
- update schemas,
- update frontend client,
- update tests.

Use consistent API response/error formats.

---

# 58. FRONTEND API RULE

All real business data must come from the backend.

Forbidden:

```typescript
const products = [
  { name: "Desk", stock: 50 }
];
```

for production functionality.

Allowed:

```text
API → React state → components
```

---

# 59. PERFORMANCE

Avoid unnecessary:

- API calls,
- full-page reloads,
- duplicate database queries,
- repeated rendering.

Use pagination for large lists.

Use debounced search where appropriate.

---

# 60. ACCESSIBILITY

Ensure:

- buttons have accessible labels,
- inputs have labels,
- keyboard navigation works,
- sufficient contrast,
- errors are visible,
- status is not communicated by color alone.

---

# 61. FINAL REVIEW CHECKLIST

Before completion:

```text
[ ] Signup creates persistent user
[ ] Login works with created user
[ ] Logout works
[ ] Forgot password works
[ ] OTP generated
[ ] OTP persisted
[ ] OTP expires
[ ] OTP cannot be reused
[ ] Password reset works
[ ] New password works for login
[ ] JWT protection works
[ ] Backend RBAC works
[ ] PostgreSQL consistency verified

[ ] Products work
[ ] Categories work
[ ] UOM works
[ ] Warehouses work
[ ] Locations work
[ ] Suppliers work
[ ] Customers work

[ ] Stock page works
[ ] On Hand works
[ ] Reserved works
[ ] Free to Use works

[ ] Receipts work
[ ] Receipt validation updates stock
[ ] Receipt ledger works
[ ] Receipt print works

[ ] Deliveries work
[ ] Delivery stock validation works
[ ] Delivery ledger works
[ ] Delivery print works

[ ] Transfers work
[ ] Transfer source/destination update
[ ] Transfer ledger works

[ ] Adjustments work
[ ] Adjustment ledger works

[ ] Move History works
[ ] Search works
[ ] Filters work
[ ] List/Kanban works
[ ] Pagination works
[ ] CSV export works

[ ] Dashboard uses real data
[ ] Late status works
[ ] Waiting status works
[ ] Dashboard counts work

[ ] Loading states work
[ ] Empty states work
[ ] Error states work
[ ] Success notifications work
[ ] Responsive UI works
[ ] Navigation works

[ ] Backend tests pass
[ ] Frontend build passes
[ ] E2E auth test passes
[ ] E2E inventory test passes
[ ] No secrets committed
[ ] No fake P0 data
```

---

# 62. FINAL HACKATHON DEMO

The final demonstration must follow:

```text
1. Signup a new user
2. Verify user exists
3. Login
4. Dashboard
5. Open Stock
6. View stock quantities
7. Open Warehouses
8. Open Locations
9. Create/inspect receipt
10. Validate receipt
11. Verify stock increase
12. Open Move History
13. Create/validate internal transfer
14. Verify location movement
15. Open Delivery
16. Validate delivery
17. Verify stock decrease
18. Perform adjustment
19. Verify ledger
20. Return to Dashboard
21. Show updated operational statistics
22. Logout
23. Forgot Password
24. Generate OTP
25. Reset password
26. Login using new password
```

Every displayed number must correspond to actual database state.

---

# 63. FAILURE RECOVERY

If the coding agent stops unexpectedly:

1. Do not restart from scratch.
2. Inspect Git status.
3. Inspect latest task file.
4. Inspect latest handoff.
5. Run tests.
6. Determine the last verified phase.
7. Continue from there.

Create handoff:

```text
.agents/handoffs/<date>-handoff.md
```

with:

```markdown
# Current State

# Completed

# In Progress

# Failed Tests

# Files Changed

# Next Action
```

---

# 64. FINAL REPORT

At completion, report:

```text
STOCKSENSE BUILD STATUS
=======================

Authentication: PASS/FAIL
Signup Persistence: PASS/FAIL
Login: PASS/FAIL
OTP: PASS/FAIL
Password Reset: PASS/FAIL
Authorization: PASS/FAIL
Database Consistency: PASS/FAIL

Products: PASS/FAIL
Warehouses: PASS/FAIL
Locations: PASS/FAIL
Receipts: PASS/FAIL
Deliveries: PASS/FAIL
Transfers: PASS/FAIL
Adjustments: PASS/FAIL
Stock: PASS/FAIL
Stock Ledger: PASS/FAIL
Dashboard: PASS/FAIL
Move History: PASS/FAIL

Search: PASS/FAIL
Filters: PASS/FAIL
Pagination: PASS/FAIL
CSV Export: PASS/FAIL
Print: PASS/FAIL
List/Kanban: PASS/FAIL

Frontend Polish: PASS/FAIL
Backend Tests: PASS/FAIL
Frontend Build: PASS/FAIL
Auth E2E: PASS/FAIL
Inventory E2E: PASS/FAIL
Demo Flow: PASS/FAIL

REMAINING ISSUES
----------------
- ...

NEXT ACTION
-----------
- ...
```

Never report PASS unless it was actually verified.

---

# 65. START NOW

Execute this specification against the EXISTING StockSense repository.

Start with:

```text
PHASE A
Codebase Audit

PHASE B
Authentication Repair

PHASE C
Authorization Verification

PHASE D
Missing Backend Function Audit

PHASE E
Missing Frontend Function Audit

PHASE F
Stock/Operations Completion

PHASE G
Frontend Polish

PHASE H
Pagination/Export/Print/List-Kanban

PHASE I
End-to-End Testing

PHASE J
Final Hackathon Review
```

**Do not skip Phase B.**

The first release-blocking objective is:

```text
SIGNUP
  ↓
USER CREATED IN DATABASE
  ↓
LOGIN
  ↓
FORGOT PASSWORD
  ↓
OTP
  ↓
PASSWORD RESET
  ↓
LOGIN WITH NEW PASSWORD
```

Only after this works should the agent proceed with the remaining missing functionality and frontend polishing.
