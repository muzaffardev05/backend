from datetime import datetime

from sqlalchemy import null

from app.database import SessionLocal
from app.models import (
    Tender
)
from app.models.tender_chunk import TenderChunk


class DatabaseService:

    def __init__(self):
        self.db = SessionLocal()

    def get_or_create(self, model, **kwargs):

        instance = self.db.query(model).filter_by(**kwargs).first()

        if instance:
            return instance

        instance = model(**kwargs)

        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)

        return instance

    def save_tender(self, tender):



        # Duplicate check
        existing = self.db.query(Tender).filter_by(
            tender_no=tender["tender_no"]
        ).first()

        if existing:
            print(f"Already exists : {tender['tender_no']}")
            return existing


        publish_date = datetime.strptime(
            tender["publish_date"], "%b %d, %Y"
        )
        closing_date = datetime.strptime(
            tender["closing_date"], "%b %d, %Y %I:%M %p"
        ) if tender["closing_date"] else None

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

            source_url=tender["source_url"],

            created_at=datetime.now(),
            updated_at=datetime.now(),
            last_scraped=datetime.now()
        )

        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)

        print(f"Inserted : {obj.tender_no}")

        return obj
    





    def save_chunks(self, chunks):
        
    

        now = datetime.now()

        objects = []

        for chunk in chunks:
            objects.append(
                TenderChunk(
                    tender_id=chunk["tender_id"],
                    chunk_index=chunk["chunk_index"],
                    chunk_text=chunk["text"],
                    created_at=now,
                    updated_at=now,
                )
            )

        self.db.bulk_save_objects(objects)
        self.db.commit()

        return len(objects)

    # def save_scraper_log(self,log_data):
    #         """
    #         Save scraper log data to the database.
    #         """
    #         try:
                
    #             log_entry = ScraperLog(**log_data)
    #             self.db.add(log_entry)
    #             self.db.commit()
    #             self.db.refresh(log_entry)
    #             print(f"Scraper log saved: {log_entry.id}")
    #             return log_entry
    #         except Exception as e:
    #             self.db.rollback()
    #             print(f"Error saving scraper log: {e}")
    #             return None
    