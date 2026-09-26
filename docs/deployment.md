# StockSense Deployment & Local Setup Guide

## Local Environment Prerequisites
- Python 3.12+
- Node.js 20+ & npm
- PostgreSQL 18

## Local Setup

### 1. Database
Create PostgreSQL database:
```sql
CREATE DATABASE stocksense_db;
```

### 2. Backend
```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
alembic upgrade head
python ../scripts/seed_database.py
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend
```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173`.
