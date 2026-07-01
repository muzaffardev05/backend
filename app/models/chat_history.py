

from sqlalchemy import Column, ForeignKey,Integer,DateTime,Text
from app.base import Base
class ChatHistory(Base):

    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer,
                     ForeignKey("users.id"))

    question = Column(Text)

    answer = Column(Text)

    created_at = Column(DateTime)