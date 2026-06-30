from sqlalchemy import Column,Integer,String,DateTime
from base import Base
class ScraperLog(Base):

    __tablename__ = "scraper_logs"

    id = Column(Integer, primary_key=True)

    website_id = Column(Integer)

    started_at = Column(DateTime)

    finished_at = Column(DateTime)

    total_found = Column(Integer)

    new_records = Column(Integer)

    updated_records = Column(Integer)

    failed_records = Column(Integer)

    status = Column(String(50))