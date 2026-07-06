from datetime import datetime
import hashlib
import logging

from app.database import SessionLocal
from app.models import (
    Tender
)

logger = logging.getLogger(__name__)


class DatabaseService:

    def __init__(self):
        self.db = SessionLocal()

 

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        if exc_type:
            self.rollback()

        self.close()



    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def flush(self):
        self.db.flush()

    def close(self):
        self.db.close()



    def calculate_hash(self, text: str) -> str:

        return hashlib.sha256(
            text.encode("utf-8")
        ).hexdigest()







    def save_tender(self, tender,document):

        now = datetime.now()

        publish_date = datetime.strptime(
            tender["publish_date"],
            "%b %d, %Y"
        )

        closing_date = (
            datetime.strptime(
                tender["closing_date"],
                "%b %d, %Y %I:%M %p"
            )
            if tender["closing_date"]
            else None
        )

        try:

            existing = (
                self.db.query(Tender)
                .filter(
                    Tender.tender_no == tender["tender_no"]
                )
                .first()
            )



            if existing:

                existing.website = tender["website"]
                existing.organization = tender["organization"]
                existing.department = tender["department"]
                existing.category = tender["category"]

                existing.reference_number = tender["reference_number"]

                existing.title = tender["title"]

                existing.publish_date = publish_date
                existing.closing_date = closing_date

                existing.location = tender["location"]

                existing.status = tender["status"]
                existing.document = document

                existing.source_url = tender["source_url"]

                existing.last_scraped = now
                existing.updated_at = now

                self.commit()

                logger.info(
                    "Updated tender %s",
                    existing.tender_no
                )

                return existing


            obj = Tender(

                website=tender["website"],

                organization=tender["organization"],

                department=tender["department"],

                category=tender["category"],

                reference_number=tender["reference_number"],

                tender_no=tender["tender_no"],

                title=tender["title"],

                publish_date=publish_date,

                closing_date=closing_date,

                location=tender["location"],

                status=tender["status"],
                document=document,

                source_url=tender["source_url"],

                content_hash=None,

                created_at=now,

                updated_at=now,

                last_scraped=now
            )

            self.db.add(obj)

            self.commit()

            self.db.refresh(obj)

            logger.info(
                "Inserted tender %s",
                obj.tender_no
            )

            return obj

        except Exception:

            self.rollback()

            logger.exception(
                "Failed saving tender %s",
                tender.get("tender_no")
            )

            raise



    def tender_changed(self, tender_no):

        tender = (
            self.db.query(Tender)
            .filter(Tender.tender_no == tender_no)
            .first()
        )

        if not tender:
            return False

        new_hash = self.calculate_hash(tender.document)

        if tender.content_hash == new_hash:
            return False

        tender.content_hash = new_hash
        tender.embedded = False
        tender.updated_at = datetime.now()

        self.commit()

        return True



   
    def get_unembedded_tenders(self, batch_size=500, offset=0):

        rows = (
            self.db.query(
                Tender.id,
                Tender.title,
                Tender.organization,
                Tender.publish_date,
                Tender.closing_date,
                Tender.location,
                Tender.status,
                Tender.category,
                Tender.tender_no,
                Tender.document,
            )
            .filter(Tender.embedded.is_(False))
            .limit(batch_size)
            .offset(offset)
            .all()
        )

        return [
            {
                "id": row.id,
                "title": row.title,
                "organization": row.organization,
                "publish_date": row.publish_date,
                "closing_date": row.closing_date,
                "location": row.location,
                "status": row.status,
                "category": row.category,
                "tender_id": row.tender_no,
                "text": row.document,
            }
            for row in rows
        ]

    def mark_tenders_as_embedded(self, ids):

        if not ids:
            return 0

        try:

            updated = (

                self.db.query(Tender)

                .filter(
                    Tender.id.in_(ids)
                )

                .update(

                    {
                        Tender.embedded: True
                    },

                    synchronize_session=False
                )

            )

            self.commit()

            return updated

        except Exception:

            self.rollback()

            logger.exception(
                "Failed updating embedded status"
            )

            raise



    def total_tenders(self):

        return (
            self.db.query(Tender)
            .count()
        )

  
    def total_unembedded_tenders(self):

        return (

            self.db.query(Tender)

            .filter(
                Tender.embedded == False
            )

            .count()

        )