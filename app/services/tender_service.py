import math
from datetime import datetime
from app.database import SessionLocal
from app.models.tender import Tender
from sqlalchemy import or_
import math

class TenderService:

    def __init__(self):
        self.db = SessionLocal()

    def get_tenders(
        self,
        page: int = 1,
        page_size: int = 20
    ):

        query = self.db.query(Tender)

        total = query.count()

        tenders = (
            query
            .order_by(Tender.publish_date.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        items = []

        for tender in tenders:

            items.append({
                "id": tender.id,
                "title": tender.title,
                "organization": tender.organization,
                "category": tender.category,
                "location": tender.location,
                "publish_date": tender.publish_date,
                "closing_date": tender.closing_date,
                "status": tender.status
            })

        return {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": math.ceil(total / page_size),
            "items": items
        }
    def get_tender(self, tender_id: int):

        tender = (
            self.db.query(Tender)
            .filter(Tender.id == tender_id)
            .first()
        )

        if tender is None:
            return None

        return {
            "id": tender.id,
            "website": tender.website,
            "organization": tender.organization,
            "department": tender.department,
            "category": tender.category,
            "reference_number": tender.reference_number,
            "tender_no": tender.tender_no,
            "title": tender.title,
            "publish_date": tender.publish_date,
            "closing_date": tender.closing_date,
            "location": tender.location,
            "status": tender.status,
            "document": tender.document,
            "source_url": tender.source_url,
            "created_at": tender.created_at,
            "updated_at": tender.updated_at
        }
    def close(self):
        self.db.close()


    def search_tenders(
        self,
        query: str,
        page: int = 1,
        page_size: int = 20
    ):

        db_query = (
            self.db.query(Tender)
            .filter(
                or_(
                    Tender.title.ilike(f"%{query}%"),
                    Tender.organization.ilike(f"%{query}%"),
                    Tender.department.ilike(f"%{query}%"),
                    Tender.category.ilike(f"%{query}%"),
                    Tender.location.ilike(f"%{query}%"),
                    Tender.tender_no.ilike(f"%{query}%"),
                    Tender.reference_number.ilike(f"%{query}%")
                )
            )
        )

        total = db_query.count()

        tenders = (
            db_query
            .order_by(Tender.publish_date.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        items = []

        for tender in tenders:

            items.append({
                "id": tender.id,
                "title": tender.title,
                "organization": tender.organization,
                "category": tender.category,
                "location": tender.location,
                "publish_date": tender.publish_date,
                "closing_date": tender.closing_date,
                "status": tender.status
            })

        return {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": math.ceil(total / page_size) if total else 0,
            "items": items
        }       

    def filter_tenders(
        self,
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

        query = self.db.query(Tender)

        if category:
            query = query.filter(Tender.category.ilike(f"%{category}%"))

        if organization:
            query = query.filter(Tender.organization.ilike(f"%{organization}%"))

        if location:
            query = query.filter(Tender.location.ilike(f"%{location}%"))

        if status:
            query = query.filter(Tender.status.ilike(status))

        if publish_from:
            query = query.filter(Tender.publish_date >= publish_from)

        if publish_to:
            query = query.filter(Tender.publish_date <= publish_to)

        if closing_from:
            query = query.filter(Tender.closing_date >= closing_from)

        if closing_to:
            query = query.filter(Tender.closing_date <= closing_to)

        sortable_columns = {
            "publish_date": Tender.publish_date,
            "closing_date": Tender.closing_date,
            "title": Tender.title,
            "organization": Tender.organization,
            "category": Tender.category,
            "location": Tender.location
        }

        sort_column = sortable_columns.get(sort_by, Tender.publish_date)

        if sort_order.lower() == "asc":
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

        total = query.count()

        tenders = (
            query
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        items = []

        for tender in tenders:
            items.append({
                "id": tender.id,
                "title": tender.title,
                "organization": tender.organization,
                "category": tender.category,
                "location": tender.location,
                "publish_date": tender.publish_date,
                "closing_date": tender.closing_date,
                "status": tender.status
            })

        return {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": math.ceil(total / page_size) if total else 0,
            "items": items
        }        