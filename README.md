# Warmup SaaS

This repository scaffolds the foundations of the Warmup SaaS platform. It currently provides a Python/FastAPI backend with SQLAlchemy models, versioned API routers, Alembic migrations, and an initial React frontend served through Docker-based infrastructure.

## Requirements

- Docker & Docker Compose
- Python 3.11
- Node.js 18

## Quickstart

Run the stack with Docker Compose from the repository root:

```bash
docker compose -f ops/docker-compose.yml up -d db redis
docker compose -f ops/docker-compose.yml run --rm backend alembic upgrade head
docker compose -f ops/docker-compose.yml up -d backend worker
# (optional Caddy/frontend proxy)
docker compose -f ops/docker-compose.yml up -d caddy
```

## Run backend manually (without Docker)

To run the FastAPI backend directly on your machine:

1. Open a terminal (CMD/PowerShell) in the `backend` directory.
2. Create and activate the virtual environment:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
   ```
3. Install dependencies and start the development server:
   ```bash
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```
4. Visit <http://127.0.0.1:8000/static/index.html> in your browser to use the built-in UI.

## Key endpoints

- `GET /api/v1/users`
- `POST /api/v1/users`
- `GET /api/v1/accounts`
- `POST /api/v1/accounts`
- `GET /api/v1/tasks`
- `POST /api/v1/tasks`
- `POST /api/v1/tasks/queue`

## Local URLs

- API Docs: <http://localhost:8000/docs>
- UI (React dev): <http://localhost:5173>
- UI (Static build TBD): `/ui`

## Project structure

```
backend/          # FastAPI application, database layer, Alembic configuration
frontend/         # React app (Vite + TypeScript)
ops/              # Dockerfiles, compose stack, and edge proxy configuration
tests/            # Automated test suites
```

## Development notes

- Backend dependencies are managed in `backend/requirements.txt` and target Python 3.11.
- Database migrations use Alembic via the configuration under `backend/alembic/`.
- The React frontend (Vite) lives in `frontend/` with scripts defined in `package.json`.
- Tests currently cover backend smoke checks in `tests/backend/` and are executed with `pytest`.
