from pydantic import BaseModel
from datetime import datetime

class OverviewItem(BaseModel):
    count: int
    change: int | None = None
    trend: str | None = None




class DashboardOverviewResponse(BaseModel):
    total_tenders: OverviewItem
    today_tenders: OverviewItem
    closing_soon: OverviewItem
    saved_tenders: OverviewItem
  


class RecentTenderItem(BaseModel):
    id: int
    status: str
    title: str
    organization: str
    publish_date: datetime 
    closing_date: datetime

    location:str 
 

class RecentTenderResponse(BaseModel):
    items: list[RecentTenderItem]