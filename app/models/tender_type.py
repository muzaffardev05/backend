
from sqlalchemy import Column,Integer,String
from base import Base
class TenderType(Base):

    __tablename__ = "tender_types"

    id = Column(Integer, primary_key=True)

    name = Column(String(50))