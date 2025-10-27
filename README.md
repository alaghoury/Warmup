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
uvicorn app.main:app --reload
```

The API will be available at http://127.0.0.1:8000. Test it with:

```bash
curl http://127.0.0.1:8000/
```

### Docker

You can also run the backend with Docker:

```bash
cd backend
docker build -t warmup-backend .
docker run --rm -p 8000:8000 warmup-backend
```

## Available endpoints

- `GET /` – returns `{ "message": "Warmup API OK" }`
- `GET /health` – returns a simple health status payload
