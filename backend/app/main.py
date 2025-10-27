from fastapi import FastAPI

app = FastAPI(title="Warmup API")


@app.get("/")
def read_root():
    return {"message": "Warmup API OK"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
