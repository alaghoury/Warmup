from fastapi import FastAPI

app = FastAPI(title="Warmup API", version="0.1.0")


@app.get("/", summary="Service heartbeat")
def read_root() -> dict[str, str]:
    """Return a simple payload confirming that the API is running."""

    return {"message": "Warmup API OK"}


@app.get("/health", summary="Health check")
def health_check() -> dict[str, str]:
    """Return a health indicator for monitoring purposes."""

    return {"status": "healthy"}
