from sqlalchemy import Column,Integer,String,Boolean,DateTime
from base import Base
class Website(Base):
    __tablename__='websites'
    id=Column(Integer,primary_key=True)
    name=Column(String(100),nullable=False)
    base_url=Column(String(255))
    country=Column(String(100))
    status=Column(Boolean,default=True)
    created_at=Column(DateTime)
    updated_at=Column(DateTime)
