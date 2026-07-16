
from sqlalchemy import Boolean, Column,Integer,String,DateTime,Text
from app.base import Base
class Tender(Base):

    __tablename__ = "tenders"

    id = Column(Integer, primary_key=True)

    website = Column(Text)

    organization= Column(Text)

    department = Column(Text)

    category = Column(Text)

    reference_number = Column(String(500))

    tender_no = Column(String(500),unique=True)

    title = Column(String(500))

    publish_date = Column(DateTime)

    closing_date = Column(DateTime)

    location = Column(String(200))

    status = Column(
       String(200)
    )
    document = Column(Text)
    source_url = Column(Text)
    embedded = Column(Boolean, default=False)

    content_hash = Column(String(64))

    last_scraped = Column(DateTime)

    created_at = Column(DateTime)

    updated_at = Column(DateTime)