from sqlalchemy import Column, ForeignKey,Integer,String,DateTime
from app.base import Base
class TenderChunk(Base):

    __tablename__ = "tender_chunks"

    id = Column(Integer, primary_key=True)

    tender_id = Column(String(255), ForeignKey("tenders.tender_no"))



    chunk_index = Column(Integer)
    chunk_text = Column(String(2000))

    created_at = Column(DateTime)
    updated_at = Column(DateTime)