from fastapi import FastAPI
from app.database import init_db
from app.api.dashboard import router as dashboard_router

app = FastAPI(
    title="Tender AI API",
    version="1.0.0"
)

app.include_router(
    dashboard_router,
    prefix="/api/v1"
)


init_db()
print("Database initialized.")
