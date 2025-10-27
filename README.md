# Warmup Backend

This repository contains a minimal FastAPI backend located under the [`backend/`](backend/) directory.

## Getting started

### Prerequisites

- Python 3.11+
- [pip](https://pip.pypa.io/)

### Setup and run locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\\Scripts\\activate`
pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at http://127.0.0.1:8000. Test it with:

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/health
```

### Docker

You can also run the backend with Docker:

```bash
cd backend
docker build -t warmup-backend .
docker run --rm -p 8000:8000 warmup-backend
```

### Docker Compose

The repository ships with a [`docker-compose.yml`](docker-compose.yml) that builds and runs the backend service in development mode with auto-reload.

```bash
docker compose up --build
```

This exposes the API on port `8000` and uses the `DATABASE_URL` environment variable configured in the compose file (pointing to the SQLite database shipped with the project).

## Available endpoints

- `GET /` – returns `{ "message": "Warmup API OK" }`
- `GET /health` – returns `{ "status": "healthy" }`
