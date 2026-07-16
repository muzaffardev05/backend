from fastapi import APIRouter, HTTPException

from app.schemas.dashboard import DashboardOverviewResponse
from app.services.dashboard_service import DashboardService
from app.schemas.dashboard import RecentTenderResponse
from app.schemas.dashboard import CategoryDistributionResponse
from app.schemas.dashboard import ActivityResponse
router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get(
    "/overview",
    response_model=DashboardOverviewResponse,
    summary="Dashboard Overview"
)
async def get_dashboard_overview():
    service = DashboardService()
    try:
        return service.get_overview()
    finally:
        service.close()


@router.get(
    "/category-distribution",
    response_model=CategoryDistributionResponse,
    summary="Category Distribution"
)
async def category_distribution():
    service = DashboardService()
    try:
        return service.get_category_distribution()
    finally:
        service.close()


@router.get(
    "/recent-tenders",
    response_model=RecentTenderResponse,
    summary="Recent Tenders"
)
async def get_recent_tenders(limit: int = 5):
    service = DashboardService()
    try:
        return service.get_recent_tenders(limit)
    finally:
        service.close()


@router.get(
    "/activity",
    response_model=ActivityResponse,
    summary="Activity"
)
async def get_activity(months: int = 12):
    service = DashboardService()
    try:
        return service.get_activity(months)
    finally:
        service.close()