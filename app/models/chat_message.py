

from datetime import datetime
from sqlalchemy.orm import  relationship
from sqlalchemy import Column, ForeignKey,Integer,DateTime, String,Text
from app.base import Base
class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)

    session_id = Column(
        Integer,
        ForeignKey("chat_sessions.id"),
        nullable=False
    )

    role = Column(String(20), nullable=False)
    # user
    # assistant

    content = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship(
        "ChatSession",
        back_populates="messages"
    )