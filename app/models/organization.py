from sqlalchemy import Column, ForeignKey,Integer,String
from base import Base
class Organization(Base):

    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True)

    website_id = Column(Integer,
                        ForeignKey("websites.id"))

    name = Column(String(200))

    city = Column(String(100))

    province = Column(String(100))