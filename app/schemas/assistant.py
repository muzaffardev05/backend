from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[int] = None


class SourceItem(BaseModel):
    tender_id: int
    title: str
    organization: str
    source_url: str


class ChatResponse(BaseModel):
    session_id: int
    answer: str
    sources: list[SourceItem] = []


class SessionItem(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime


class SessionListResponse(BaseModel):
    sessions: list[SessionItem]    


class MessageItem(BaseModel):
    role: str
    content: str
    created_at: datetime


class ConversationResponse(BaseModel):
    session_id: int
    title: str
    messages: list[MessageItem]    


class DeleteResponse(BaseModel):
    message: str    