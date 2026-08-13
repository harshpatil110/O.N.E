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
        from app.core.langgraph_agent import app_graph
        from app.core.task_manager import get_next_task
        from app.models.user import User
        from langchain_core.messages import HumanMessage, AIMessage
        from datetime import datetime, timezone
        
        # Action 5.1: Fetch User Data
        user_model = db.query(User).filter(User.id == current_user.id).first()
        if not user_model:
            raise HTTPException(status_code=404, detail="User not found")
            
        current_task_obj = get_next_task(db, str(current_user.id))
        current_task_string = current_task_obj.title if current_task_obj else "No pending tasks."
        
        # Action 5.1: Fetch Chat History (last 10 messages)
        history_logs = db.query(ConversationLog)\
            .filter_by(session_id=session_id)\
            .filter(ConversationLog.role != "system")\
            .order_by(ConversationLog.created_at.asc())\
            .limit(10)\
            .all()
            
        # Action 5.2: Format Messages to LangChain classes
        formatted_messages = []
        for log in history_logs:
            if log.role == "user":
                formatted_messages.append(HumanMessage(content=log.content))
            elif log.role == "assistant":
                formatted_messages.append(AIMessage(content=log.content))
                
        # Append the new incoming message
        formatted_messages.append(HumanMessage(content=request.message))
        
        # End the current transaction so connection can be recycled if needed
        db.commit()
        
        # Action 5.2: State Initialization
        initial_state = {
            "messages": formatted_messages,
            "user_id": str(user_model.id),
            "user_role": user_model.department_role,
            "progress": user_model.onboarding_progress,
            "current_task": current_task_string,
            "next_route": ""
        }
        
        # Invoke the compiled LangGraph workflow
        response_state = app_graph.invoke(initial_state)
        
        # Extract the final AI response
        final_messages = response_state.get("messages", [])
        if final_messages and hasattr(final_messages[-1], "content"):
            reply = str(final_messages[-1].content)
        else:
            reply = "I'm sorry, I couldn't process that request."
        
        # 4. Database Persistence (Save new human and AI messages)
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
