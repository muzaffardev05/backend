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
   


    def get_category_distribution(self):

        total = (
            self.db.query(func.count(Tender.id))
            .scalar()
        )

        categories = (
            self.db.query(
                Tender.category,
                func.count(Tender.id).label("count")
            )
            .group_by(Tender.category)
            .order_by(func.count(Tender.id).desc())
            .all()
        )

        items = []
        other_count = 0

        for index, (category, count) in enumerate(categories):

            if index < 4:
                items.append({
                    "category": category if category else "Other",
                    "percentage": round((count / total) * 100)
                })
            else:
                other_count += count

        if other_count > 0:
            items.append({
                "category": "Other",
                "percentage": round((other_count / total) * 100)
            })

        return {
            "items": items
        }
    
    def get_activity(self, months: int = 12):

        current_year = datetime.now().year

        results = (
            self.db.query(
                func.month(Tender.publish_date).label("month"),
                func.count(Tender.id).label("count")
            )
            .filter(func.year(Tender.publish_date) == current_year)
            .group_by(func.month(Tender.publish_date))
            .order_by(func.month(Tender.publish_date))
            .all()
        )

        month_names = {
            1: "Jan",
            2: "Feb",
            3: "Mar",
            4: "Apr",
            5: "May",
            6: "Jun",
            7: "Jul",
            8: "Aug",
            9: "Sep",
            10: "Oct",
            11: "Nov",
            12: "Dec",
        }

        data = {month: count for month, count in results}

        start_month = max(1, datetime.now().month - months + 1)

        items = []

        for month in range(start_month, datetime.now().month + 1):

            items.append({
                "month": month_names[month],
                "tenders": data.get(month, 0),
                "saved": 0
            })

        return {
            "items": items
        }
    
    def close(self):
        self.db.close()