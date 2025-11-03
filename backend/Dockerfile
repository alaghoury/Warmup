# Use official lightweight Python
FROM python:3.11-slim

# rebuild trigger codex 2025-10-31-r47e0v
WORKDIR /app
COPY backend/requirements.txt ./requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libffi-dev libssl-dev python3-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y build-essential python3-dev && \
    rm -rf /var/lib/apt/lists/*
COPY backend/app ./app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
