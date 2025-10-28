# Warmup SaaS

A minimal full-stack SaaS starter featuring a FastAPI backend and a Vite + React frontend. The stack ships with authentication, subscription plans, usage tracking, and analytics-ready endpoints backed by SQLite for local development (switchable to Postgres by updating `DATABASE_URL`).

## Requirements

- Python 3.11
- Node.js 18+
- (Optional) Docker & Docker Compose for Postgres development

## Backend setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API is served at <http://127.0.0.1:8000>. Interactive docs are available at <http://127.0.0.1:8000/docs>.

## Frontend setup

```bash
cd frontend
npm install
npm run dev
```

The frontend dev server runs at <http://localhost:5173> and talks to the backend using the `VITE_API_URL` environment variable (defaults to `http://127.0.0.1:8000/api`).

## Environment variables

Copy `.env.example` to `.env` and adjust values as needed. SQLite is used by default; swap `DATABASE_URL` for a Postgres connection string when deploying.

## Optional Postgres via Docker

```bash
docker compose up -d db
```

Update `DATABASE_URL` to point at the running Postgres container to persist data externally.

## Project structure

```
backend/
  app/
    routes/        # FastAPI routers (auth, users, subscriptions, analytics)
    schemas.py     # Pydantic models for request/response payloads
    utils.py       # Password hashing & JWT helpers
    deps.py        # Shared dependencies (DB + auth)
frontend/
  src/
    components/    # React UI widgets (auth, billing, analytics, etc.)
    lib/           # Auth helpers
```

## Features

- JWT-based authentication (register/login/logout)
- Subscription plans with checkout switching and usage caps
- Usage metrics & analytics summaries
- React dashboard with tabs for users, usage, billing, and analytics
