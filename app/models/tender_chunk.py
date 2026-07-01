from sqlalchemy import Column, ForeignKey,Integer,String,DateTime
from app.base import Base
class TenderChunk(Base):

    __tablename__ = "tender_chunks"

    id = Column(Integer, primary_key=True)

    tender_id = Column(Integer,
                       ForeignKey("tenders.id"))

    document_id = Column(Integer,
                         ForeignKey("documents.id"))

    chunk_number = Column(Integer)

    vector_id = Column(String(200), unique=True)

    created_at = Column(DateTime)