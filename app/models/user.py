
from datetime import datetime
from sqlalchemy.orm import  relationship
from sqlalchemy import Column,Integer,String,DateTime
from app.base import Base
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True)
    created_at = Column(DateTime, default=datetime.now)

    sessions = relationship("ChatSession", back_populates="user")