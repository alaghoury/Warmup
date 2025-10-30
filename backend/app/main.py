from fastapi import FastAPI
from app.startup import seed_superuser

app = FastAPI()

@app.on_event("startup")
def on_startup():
    print("🚀 Application starting...")
    try:
        seed_superuser()
        print("✅ Superuser seeding complete.")
    except Exception as e:
        print(f"⚠️ Error during startup: {e}")

@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
