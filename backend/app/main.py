from fastapi import FastAPI
from app.startup import apply_migrations, seed_superuser

app = FastAPI()


@app.on_event("startup")
def startup() -> None:
    print("🚀 Application starting...")
    apply_migrations()
    seed_superuser()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
