from fastapi import FastAPI
from app.database import init_db
from app.api.dashboard import router as dashboard_router
from app.api.tenders import router as tender_router
from app.api.assistant import router as assistant_router
app = FastAPI(
    title="Tender AI API",
    version="1.0.0"
)

app.include_router(
    dashboard_router,
    prefix="/api/v1"
)
app.include_router(
    tender_router,
    prefix="/api/v1"
)
app.include_router(
    assistant_router,
    prefix="/api/v1"
)

init_db()
print("Database initialized.")
