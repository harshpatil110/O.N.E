from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.core.auth_deps import get_current_user
from app.models.conversation_log import ConversationLog
from app.models.onboarding_session import OnboardingSession
from app.agents.orchestrator import AgentOrchestrator
from app.schemas.auth import UserResponse
from app.schemas.chat import ConversationHistoryResponse, MessageResponse

router = APIRouter()

class ChatMessageRequest(BaseModel):
    message: str

class ChatMessageResponse(BaseModel):
    reply: str
    session_id: str

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
    # Optional security check here
    session_obj = db.query(OnboardingSession).filter(OnboardingSession.id == session_id).first()
    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found")
    if str(session_obj.user_id) != str(current_user.id) and current_user.role != "hr_admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    try:
        orchestrator = AgentOrchestrator(session_id=session_id, db=db)
        reply = await orchestrator.handle_message(request.message)
        return ChatMessageResponse(reply=reply, session_id=session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat/{session_id}/history", response_model=ConversationHistoryResponse)
async def get_chat_history(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Fetch conversation history for a specific session.
    """
    session_obj = db.query(OnboardingSession).filter(OnboardingSession.id == session_id).first()
    
    if not session_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
        
    if str(session_obj.user_id) != str(current_user.id) and current_user.role != "hr_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Forbidden: Cannot access another user's session history"
        )

    logs = db.query(ConversationLog)\
        .filter(ConversationLog.session_id == session_id)\
        .filter(ConversationLog.role != "system")\
        .order_by(ConversationLog.created_at.asc())\
        .all()
    
    messages = [
        MessageResponse(role=log.role, content=log.content, created_at=log.created_at)
        for log in logs
    ]
    
    return ConversationHistoryResponse(session_id=session_id, messages=messages)
