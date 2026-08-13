import uuid
from typing import Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.core.database import get_db
from app.core.auth_deps import get_current_user
from app.services.checklist_service import ChecklistService

from app.models.onboarding_session import OnboardingSession
from app.models.conversation_log import ConversationLog
from app.schemas.auth import UserResponse
from app.schemas.onboarding import SessionStartResponse, SessionDetailResponse, SessionProgressResponse

router = APIRouter()

@router.post("/onboarding/start", response_model=SessionStartResponse)
async def start_session(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Starts a new onboarding session for the current user.
    If an active session already exists, returns the existing one.
    """
    welcome_msg = ("Hi! I'm O.N.E — your Onboarding Navigation Environment. "
                   "I'm here to guide you through your first days at the company. "
                   "Let's start with the basics — what's your full name?")

    # Check for existing active session
    existing_session = db.query(OnboardingSession).filter(
        OnboardingSession.user_id == str(current_user.id),
        OnboardingSession.status == "in_progress"
    ).first()
    
    if existing_session:
        # Ensure the welcome log exists (idempotent)
        has_logs = db.query(ConversationLog).filter(
            ConversationLog.session_id == existing_session.id
        ).first()
        if not has_logs:
            db.add(ConversationLog(
                session_id=str(existing_session.id),
                role="assistant",
                content=welcome_msg,
                created_at=datetime.now(timezone.utc)
            ))
            db.commit()
        return SessionStartResponse(
            session_id=str(existing_session.id),
            message=welcome_msg
        )

    # Generate a unique ID
    new_session_id = str(uuid.uuid4())
    
    # Create a new session object
    new_session = OnboardingSession(
        id=new_session_id,
        user_id=str(current_user.id),
        status="in_progress",
        current_fsm_state="WELCOME",
        started_at=datetime.now(timezone.utc)
    )
    
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    
    # Persist welcome message as conversation log so the 3-question gate stays in sync
    db.add(ConversationLog(
        session_id=new_session_id,
        role="assistant",
        content=welcome_msg,
        created_at=datetime.now(timezone.utc)
    ))
    db.commit()
    
    return SessionStartResponse(
        session_id=str(new_session.id),
        message=welcome_msg
    )

@router.get("/onboarding/{session_id}", response_model=SessionDetailResponse)
async def get_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Retrieve session details by ID. Validates user owns the session OR is hr_admin.
    """
    session_obj = db.query(OnboardingSession).filter(OnboardingSession.id == session_id).first()
    
    if not session_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Session not found"
        )
        
    # Authorization checks
    if str(session_obj.user_id) != str(current_user.id) and current_user.role != "hr_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Forbidden: Cannot access another user's session unless you are an HR Admin"
        )
        
    return session_obj

@router.get("/onboarding/{session_id}/progress", response_model=SessionProgressResponse)
async def get_progress(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Retrieve onboarding checklist progress summary for a given session.
    """
    session_obj = db.query(OnboardingSession).filter(OnboardingSession.id == session_id).first()
    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found")
        
    if str(session_obj.user_id) != str(current_user.id) and current_user.role != "hr_admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    checklist_service = ChecklistService(db)
    return await checklist_service.get_progress(session_id)
