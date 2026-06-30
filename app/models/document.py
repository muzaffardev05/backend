
from sqlalchemy import BigInteger, Column, ForeignKey,Integer,String,Boolean,DateTime, Text
from base import Base

class Document(Base):

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)

    tender_id = Column(Integer,
                       ForeignKey("tenders.id"))

    file_name = Column(String(255))

    file_path = Column(Text)

    file_type = Column(String(20))

    pages = Column(Integer)

    file_size = Column(BigInteger)

    processed = Column(Boolean)

    uploaded_at = Column(DateTime)