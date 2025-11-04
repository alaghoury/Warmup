# Use official Python 3.11 image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy backend requirements and install dependencies
COPY backend/requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libffi-dev libssl-dev python3-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y build-essential python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy the rest of the backend app
COPY backend/app ./app

# Expose FastAPI default port
EXPOSE 8000

# Launch FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
