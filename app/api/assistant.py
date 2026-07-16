from fastapi import APIRouter

from app.schemas.assistant import (
    ChatRequest,
    ChatResponse,
    SessionListResponse,
    ConversationResponse,
    DeleteResponse
)

from app.services.assistant_service import AssistantService


router = APIRouter(
    prefix="/assistant",
    tags=["AI Assistant"]
)


@router.post(
    "/chat",
    response_model=ChatResponse
)
async def chat(request: ChatRequest):

    service = AssistantService()

    try:

        return service.chat(
            user_id=1,
            session_id=request.session_id,
            message=request.message
        )

    finally:
        service.close()


@router.get(
    "/sessions",
    response_model=SessionListResponse,
    summary="List Chat Sessions"
)
async def get_sessions():

    service = AssistantService()

    try:
        return service.get_sessions(user_id=1)

    finally:
        service.close()

@router.get(
    "/sessions/{session_id}",
    response_model=ConversationResponse,
    summary="Get Conversation"
)
async def get_conversation(session_id: int):

    service = AssistantService()

    try:
        return service.get_conversation(session_id)

    finally:
        service.close()        



@router.delete(
    "/sessions/{session_id}",
    response_model=DeleteResponse,
    summary="Delete Chat Session"
)
async def delete_session(session_id: int):

    service = AssistantService()

    try:
        return service.delete_session(session_id)

    finally:
        service.close()        