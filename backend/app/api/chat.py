from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.core.auth_deps import get_current_user
from app.models.conversation_log import ConversationLog
from app.agents.orchestrator import AgentOrchestrator
from app.schemas.auth import UserResponse

router = APIRouter()

class ChatMessageRequest(BaseModel):
    message: str

class ChatMessageResponse(BaseModel):
    reply: str
    session_id: str

class HistoryResponse(BaseModel):
    role: str
    content: str

@router.post("/chat/{session_id}/message", response_model=ChatMessageResponse)
async def send_message(
    session_id: str,
    request: ChatMessageRequest,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Handle incoming chat message for a specific onboarding session.
    Delegates message processing to the AgentOrchestrator.
    """
    try:
        orchestrator = AgentOrchestrator(session_id=session_id, db=db)
        reply = await orchestrator.handle_message(request.message)
        return ChatMessageResponse(reply=reply, session_id=session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat/{session_id}/history", response_model=List[HistoryResponse])
async def get_chat_history(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Fetch conversation history for a specific session.
    """
    logs = db.query(ConversationLog)\
        .filter(ConversationLog.session_id == session_id)\
        .order_by(ConversationLog.created_at.asc())\
        .all()
    
    return [HistoryResponse(role=log.role, content=log.content) for log in logs]
