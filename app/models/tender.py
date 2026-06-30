from pymysql import Date
from sqlalchemy import Column, Enum, ForeignKey,Integer,String,DateTime, Text
from base import Base
class Tender(Base):

    __tablename__ = "tenders"

    id = Column(Integer, primary_key=True)

    website_id = Column(Integer, ForeignKey("websites.id"))

    organization_id = Column(Integer, ForeignKey("organizations.id"))

    department_id = Column(Integer, ForeignKey("departments.id"))

    category_id = Column(Integer, ForeignKey("categories.id"))

    type_id = Column(Integer, ForeignKey("tender_types.id"))

    reference_number = Column(String(100), unique=True)

    tender_no = Column(String(100))

    title = Column(String(500))

    publish_date = Column(DateTime)

    closing_date = Column(DateTime)

    location = Column(String(200))

    status = Column(
        Enum("OPEN", "CLOSED", "EXPIRED")
    )

    source_url = Column(Text)

    content_hash = Column(String(64))

    last_scraped = Column(DateTime)

    created_at = Column(DateTime)

    updated_at = Column(DateTime)