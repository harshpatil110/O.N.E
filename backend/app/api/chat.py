import logging
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
from app.schemas.chat import (
    ConversationHistoryResponse, 
    MessageResponse, 
    ChatMessageRequest, 
    ChatMessageResponse
)

logger = logging.getLogger(__name__)

router = APIRouter()

# Sub-task 21.3: Ensured response_model is present for all routes

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
        from app.core.agent import run_hermes_agent
        from datetime import datetime, timezone
        
        # 1. Fetch conversation history (last 20 messages)
        history_logs = db.query(ConversationLog)\
            .filter_by(session_id=session_id)\
            .filter(ConversationLog.role != "system")\
            .order_by(ConversationLog.created_at.asc())\
            .limit(20)\
            .all()
            
        history = [
            {"role": log.role, "content": log.content}
            for log in history_logs
        ]
        
        # End the current transaction so connection can be recycled if needed
        db.commit()
        
        # 2. Invoke Hermes agent
        reply = await run_hermes_agent(request.message, history)
        
        # 3. Persist new messages to database
        now = datetime.now(timezone.utc)
        
        user_log = ConversationLog(
            session_id=session_id,
            role="user",
            content=request.message,
            created_at=now
        )
        
        ai_log = ConversationLog(
            session_id=session_id,
            role="assistant",
            content=reply,
            created_at=now
        )
        
        from app.core.database import SessionLocal
        with SessionLocal() as fresh_db:
            fresh_db.add(user_log)
            fresh_db.add(ai_log)
            fresh_db.commit()
        
        return ChatMessageResponse(content=reply, session_id=session_id)
        
    except Exception as e:
        logger.error(f"Error in chat logic: {e}", exc_info=True)
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
