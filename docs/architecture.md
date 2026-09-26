# StockSense Architecture Specification

## Architecture Overview

StockSense follows a clean layered architecture with strict separation of concerns:

```
[ Frontend: React + TypeScript + Vite + Lucide Icons ]
                      |
                 RESTful APIs
                      |
[ Backend: FastAPI (Python 3.12+) ]
  ├── Routing Layer (FastAPI Routers)
  ├── Dependency Injection (DB Sessions, Current User, Roles)
  ├── Service Layer (Business Logic, Transaction Management, Invariants)
  └── Repository / ORM Layer (SQLAlchemy 2.0 Models)
                      |
[ Database: PostgreSQL 18 ]
  ├── Relational Schema & Strict Foreign Keys
  ├── Unique & Check Constraints
  ├── Transaction Isolation & Row-level Locks (`FOR UPDATE`)
  └── Append-only Stock Movement Ledger
```

## Core Design Principles
1. **Single Source of Truth:** Stock balances are managed alongside the immutable stock ledger within single atomic transactions.
2. **Layer Isolation:** Controllers/routes never execute raw SQL or perform stock math directly.
3. **Optimistic/Pessimistic Locking:** Critical inventory state transitions acquire row-level locks on `stock_balances` during validation to prevent race conditions and overselling.
