from fastapi import FastAPI

app = FastAPI(
    title="Tender AI API",
    version="1.0.0"
)
@app.get("/")
async def health():
    return {
        "status": "healthy"
    }

