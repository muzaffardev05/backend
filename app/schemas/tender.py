from datetime import datetime

from pydantic import BaseModel


class TenderItem(BaseModel):
    id: int
    title: str
    organization: str
    category: str | None = None
    location: str | None = None
    publish_date: datetime | None = None
    closing_date: datetime | None = None
    status: str | None = None


class TenderListResponse(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int
    items: list[TenderItem]


class TenderDetailResponse(BaseModel):
    id: int
    website: str | None = None
    organization: str | None = None
    department: str | None = None
    category: str | None = None
    reference_number: str | None = None
    tender_no: str | None = None
    title: str | None = None
    publish_date: datetime | None = None
    closing_date: datetime | None = None
    location: str | None = None
    status: str | None = None
    document: str | None = None
    source_url: str | None = None
    created_at: datetime | None = None
    updated_at: datetime |None = None    