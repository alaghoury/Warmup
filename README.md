# Warmup SaaS

A full-stack SaaS starter featuring a FastAPI backend and a Vite + React frontend. The stack ships with authentication,
subscription plans, usage tracking, analytics endpoints, and an admin dashboard. SQLite backs local development, and you can
switch to Postgres by updating `DATABASE_URL`.

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

The API is served at <http://127.0.0.1:8000>. Interactive docs live at <http://127.0.0.1:8000/docs>.

### Database migrations

Alembic migrations run automatically on startup, but you can also trigger them manually:

```bash
cd backend
python -m app.cli upgrade
```

To generate a new revision based on model changes:

```bash
python -m app.cli revision "describe the change"
```

## Frontend setup

```bash
cd frontend
npm install
npm run dev
```

The frontend dev server runs at <http://localhost:5173> and reads the API base URL from `VITE_API_URL` (defaults to
`http://127.0.0.1:8000/api`).

## Environment variables

Copy `.env.example` to `.env` and adjust values as needed. Notable keys:

| Variable | Description |
| --- | --- |
| `DATABASE_URL` | SQLite by default. Point to Postgres for production (e.g. `postgresql+psycopg://warmup:warmup@db:5432/warmup`). |
| `JWT_SECRET` | Secret key for signing JWT access tokens. |
| `ADMIN_EMAIL`, `ADMIN_PASSWORD` | Initial superuser credentials seeded on startup. |
| `VITE_API_URL` | Frontend base URL for API requests. |

## Docker Compose stack

Spin up Postgres, the FastAPI backend, and the Vite frontend together:

```bash
docker compose up --build
```

The services expose:

- Backend API: <http://localhost:8000>
- API docs: <http://localhost:8000/docs>
- Frontend UI: <http://localhost:5173>

## Admin access

On startup the backend ensures an admin user exists:

- Email: `mohammedalaghoury@gmail.com`
- Password: `Moh2611`

The startup job is idempotent—it also re-promotes the account to admin, reactivates it, and resets the password if you change
those values in the database or environment configuration.

Use these credentials to log in and access the admin panel tab in the dashboard.

## Project structure

```
backend/
  app/
    core/security.py   # Password hashing & JWT helpers
    config.py          # Environment-driven settings
    database.py        # SQLAlchemy engine/session configuration
    models/            # ORM models (users, plans, subscriptions, usage)
    schemas/           # Pydantic schemas
    routes/            # FastAPI routers (auth, users, subscriptions, analytics, admin)
    deps.py            # Shared dependencies (DB session, auth guards)
    cli.py             # Alembic helpers
  alembic/             # Migration environment & revisions
frontend/
  src/
    pages/             # Auth + dashboard pages
    components/        # Dashboard widgets (users, billing, usage, analytics, admin)
    lib/               # Axios client & auth helpers
```

## Features

- JWT-based authentication (register/login/logout) with a seeded superuser
- Subscription plans with checkout switching and usage caps
- Usage metrics, analytics summaries, and admin user management (activate/deactivate)
- React dashboard with Tailwind styling, toast notifications, and admin panel tab

## Testing

```bash
pytest -q
```

> **Note:** Installing Python dependencies may require outbound internet access. If package installation is blocked the tests
> cannot run locally; CI should cover the suite instead.
