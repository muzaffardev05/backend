
from sqlalchemy import Column,Integer,String,DateTime
from app.base import Base
class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    username = Column(String(100), unique=True)

    password_hash = Column(String(255))

    role = Column(String(50))

    created_at = Column(DateTime)