from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.schemas.tender import (
    TenderListResponse,
    TenderDetailResponse
)
from app.services.tender_service import TenderService

router = APIRouter(
    prefix="/tenders",
    tags=["Tenders"]
)


@router.get(
    "",
    response_model=TenderListResponse,
    summary="List Tenders"
)
async def get_tenders(
    page: int = 1,
    page_size: int = 20
):
    service = TenderService()

    try:
        return service.get_tenders(page, page_size)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        service.close()

@router.get(
    "/search",
    response_model=TenderListResponse,
    summary="Search Tenders"
)
async def search_tenders(
    q: str,
    page: int = 1,
    page_size: int = 20
):

    service = TenderService()

    try:
        return service.search_tenders(
            query=q,
            page=page,
            page_size=page_size
        )

    finally:
        service.close()




@router.get(
    "/filter",
    response_model=TenderListResponse,
    summary="Filter Tenders"
)
async def filter_tenders(

    category: str | None = None,
    organization: str | None = None,
    location: str | None = None,
    status: str | None = None,

    publish_from: datetime | None = None,
    publish_to: datetime | None = None,

    closing_from: datetime | None = None,
    closing_to: datetime | None = None,

    sort_by: str = "publish_date",
    sort_order: str = "desc",

    page: int = 1,
    page_size: int = 20
):

    service = TenderService()

    try:
        return service.filter_tenders(
            category=category,
            organization=organization,
            location=location,
            status=status,
            publish_from=publish_from,
            publish_to=publish_to,
            closing_from=closing_from,
            closing_to=closing_to,
            sort_by=sort_by,
            sort_order=sort_order,
            page=page,
            page_size=page_size
        )

    finally:
        service.close()        




@router.get(
    "/{tender_id}",
    response_model=TenderDetailResponse,
    summary="Tender Details"
)
async def get_tender(tender_id: int):
    service = TenderService()

    try:
        tender = service.get_tender(tender_id)

        if tender is None:
            raise HTTPException(
                status_code=404,
                detail="Tender not found"
            )

        return tender

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        service.close()

