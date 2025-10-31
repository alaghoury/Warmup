# Use official lightweight Python
FROM python:3.11-slim

# force rebuild

# Workdir inside the image
WORKDIR /app

# Copy backend dependency list
COPY backend/requirements.txt ./requirements.txt

# Install system deps (build wheels if needed), then Python deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libffi-dev libssl-dev python3-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y build-essential python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy the backend app code
COPY backend/app ./app

# Expose FastAPI
EXPOSE 8000

# Launch API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
