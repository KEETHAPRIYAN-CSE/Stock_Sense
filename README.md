# StockSense - Modular Inventory Management System

StockSense is an inventory transaction system designed for high-integrity warehouse operations. Built around an **immutable, append-only Stock Movement Ledger**, every stock modification (receipt, transfer, customer delivery, or manual adjustment) is atomically verified and persisted in PostgreSQL.

## Features

- **Transactional Inventory Engine:** Race-condition-free stock changes with row-level locking.
- **Stock Movement Ledger:** Complete immutable audit log of all inventory movements.
- **Multi-Location & Warehouse Support:** Track products by warehouse, location, and aisle/rack.
- **Inbound Receipts:** Validate incoming stock directly from suppliers.
- **Outbound Deliveries:** Pick, pack, and validate workflows with stock-shortage protections.
- **Internal Transfers:** Move inventory across locations while preserving total stock invariants.
- **Inventory Adjustments:** Reconcile system records with physical inventory counts.
- **Executive Dashboard:** Live metrics for products, stockouts, and pending operations.
- **Secure Authentication:** JWT tokens, role-based access control, and hashed OTP password reset.
- **Modern Dark UI:** High-contrast responsive interface inspired by warehouse ergonomics.

---

## Tech Stack

- **Backend:** Python 3.12, FastAPI, SQLAlchemy 2.0, Alembic, PostgreSQL 18, Pydantic, Argon2 / Passlib, PyJWT
- **Frontend:** React 19, TypeScript, Vite, React Router, Lucide Icons, Axios
- **Database:** PostgreSQL 18
- **Testing:** Pytest, HTTPX, TypeScript type checking

---

## Project Structure

```text
StockSense/
├── backend/                  # FastAPI Application
│   ├── alembic/              # Database schema migrations
│   ├── app/
│   │   ├── api/              # API endpoints and route controllers
│   │   ├── core/             # Configuration, security, database session
│   │   ├── models/           # SQLAlchemy ORM models
│   │   ├── repositories/     # Data access layer
│   │   ├── schemas/          # Pydantic validation schemas
│   │   ├── services/         # Inventory engine and business logic
│   │   └── utils/            # Helper utilities
│   ├── tests/                # Automated pytest suite
│   ├── alembic.ini
│   └── requirements.txt
│
├── frontend/                 # React + TypeScript + Vite SPA
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/            # Application pages
│   │   ├── services/         # API client bindings
│   │   ├── types/            # TypeScript interfaces
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── docs/                     # Full system specifications & documentation
├── scripts/                  # Database creation and seed scripts
├── .agents/                  # Agent rules, prompts, tasks, and handoffs
└── BUILD_STOCKSENSE.md       # Master specification
```

---

## Local Setup & Quick Start

### 1. Prerequisites
- Python 3.12+
- Node.js 20+ & npm
- PostgreSQL 18 running locally

### 2. Environment Configuration
Copy `.env.example` to `.env` in the root and in `backend/`:
```bash
cp .env.example backend/.env
```
Update `DATABASE_URL` with your local PostgreSQL credentials:
```env
DATABASE_URL=postgresql+psycopg2://<username>:<password>@localhost:5432/stocksense_db
```

### 3. Backend Setup
```bash
cd backend
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# Install dependencies:
pip install -r requirements.txt

# Run migrations:
alembic upgrade head

# Seed database with sample data:
python ../scripts/seed_database.py

# Start backend server:
uvicorn app.main:app --reload --port 8000
```
API Documentation will be available at: `http://localhost:8000/docs`

### 4. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## Running Tests

### Backend Tests
```bash
cd backend
pytest -v
```

### Frontend Typecheck & Build
```bash
cd frontend
npm run build
```

---

## Default Demo Credentials
- **Inventory Manager:** `manager@stocksense.com` / `admin123`
- **Warehouse Staff:** `staff@stocksense.com` / `staff123`
