from datetime import date, timedelta,datetime
from sqlalchemy import func

from app.database import SessionLocal
from app.models.tender import Tender


class DashboardService:

    def __init__(self):
        self.db = SessionLocal()

    def get_overview(self):

        today = date.today()
        next_week = today + timedelta(days=7)
        yesterday = today - timedelta(days=1)

        total_tenders = (
            self.db.query(func.count(Tender.id))
            .scalar()
        )
        
        yesterday_total=(
            self.db.query(func.count(Tender.id))
            .filter(Tender.publish_date <= yesterday)
            .scalar()
        )
        
        total_change = total_tenders - yesterday_total
        today_tenders = (
            self.db.query(func.count(Tender.id))
            .filter(Tender.publish_date == today)
            .scalar()
        )
        yesterday_tenders = (
    self.db.query(func.count(Tender.id))
    .filter(Tender.publish_date == yesterday)
    .scalar()
)
        today_change = today_tenders - yesterday_tenders
    

        closing_soon = (
            self.db.query(func.count(Tender.id))
            .filter(
                Tender.closing_date >= today,
                Tender.closing_date <= next_week
            )
            .scalar()
        )
        yesterday_closing = (
    self.db.query(func.count(Tender.id))
    .filter(
        Tender.closing_date >= yesterday,
        Tender.closing_date <= (yesterday + timedelta(days=7))
    )
    .scalar()
)
        closing_change = closing_soon - yesterday_closing


 


        return {
            "total_tenders": {
                "count": total_tenders,
                "change": total_change,
                "trend": "up" if total_change >=0 else "down"
            },
            "today_tenders": {
                "count": today_tenders,
                "change": today_change,
                "trend": "up" if today_change >=0 else "down"
            },
            "closing_soon": {
                "count": closing_soon,
                "change":closing_change,
                "trend":"up" if closing_change >=0 else "down"
            },
            "saved_tenders": {
                "count": 0,
                "new": 0
            },
          
        }

    def get_recent_tenders(self, limit: int = 5):
            

            tenders = (
                self.db.query(Tender)
                .order_by(Tender.publish_date.desc())
                .limit(limit)
                .all()
            )

            items = []

            for tender in tenders:

                items.append({
                    "id": tender.id,
                    "status": "OPEN" if tender.closing_date >= datetime.now()else "CLOSED",
                    "title": tender.title,
                    "organization": tender.organization,
                    "publish_date": tender.publish_date,
                    "closing_date": tender.closing_date,
                    "location":tender.location

               
                })

            return {
                "items": items
            }

    def close(self):
        self.db.close()