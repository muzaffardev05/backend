from fastapi import APIRouter, HTTPException

from app.schemas.dashboard import DashboardOverviewResponse
from app.services.dashboard_service import DashboardService
from app.schemas.dashboard import RecentTenderResponse
router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get(
    "/overview",
    response_model=DashboardOverviewResponse,
    summary="Dashboard Overview"
)



@router.get(
    "/recent-tenders",
    response_model=RecentTenderResponse,
    summary="Recent Tenders"
)
async def get_recent_tenders(limit: int = 5):

    service = DashboardService()

    try:
        return service.get_recent_tenders(limit)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        service.close()
        
async def get_dashboard_overview():

    service = DashboardService()

    try:
        return service.get_overview()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        service.close()