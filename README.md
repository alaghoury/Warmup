# Warmup SaaS

This repository scaffolds the foundations of the Warmup SaaS platform. It currently provides a Python/FastAPI backend with SQLAlchemy models, versioned API routers, and Alembic migrations, along with placeholders for a future React frontend and deployment assets.

## Project structure

```
backend/          # FastAPI application, database layer, Alembic configuration
frontend/         # (placeholder) React app will live here
ops/              # Dockerfiles, compose stack, and edge proxy configuration
tests/            # Automated test suites
```

## Backend development

### Prerequisites

- Python 3.11+
- [pip](https://pip.pypa.io/)

### Run locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API root responds with:

```bash
curl http://127.0.0.1:8000/
# {"message": "Warmup SaaS OK"}
```

Versioned endpoints are available under `/api/v1`, for example `GET /api/v1/users`, `POST /api/v1/accounts`, and `POST /api/v1/tasks`.

### Database migrations

Alembic is configured under `backend/alembic/`. To create and run migrations:

```bash
cd backend
alembic revision -m "describe change"
alembic upgrade head
```

Ensure the `DATABASE_URL` environment variable is set, otherwise the default Postgres connection from `app.config.Settings` is used.

### Docker and Compose stack

The `ops/` directory centralizes container tooling.

- Build and run the backend container only:
  ```bash
  docker build -f ops/Dockerfile.backend -t warmup-backend ..
  docker run --rm -p 8000:8000 warmup-backend
  ```
- Start the full stack (Postgres, Redis, backend, worker, placeholder frontend, Caddy proxy):
  ```bash
  cd ops
  docker compose up --build
  ```

## Frontend placeholder

A future React application will be mounted under `backend/app/static` and surfaced through the `/ui` redirect once assets are added. For now the directory only contains a `.gitkeep` marker to track the path.

## Tests

Placeholder tests live in `tests/backend/`. Run them with your preferred test runner (e.g. `pytest`). Additional coverage will be added as features mature.
