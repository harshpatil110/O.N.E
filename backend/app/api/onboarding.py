import uuid
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.core.database import get_db
from app.core.auth_deps import get_current_user
from app.services.checklist_service import ChecklistService

# Attempt to import models if they exist, else provide fallback
try:
    from app.models.session import OnboardingSession
except ImportError:
    # Placeholder class if missing
    class OnboardingSession:
        pass

from app.schemas.auth import UserResponse

router = APIRouter()

@router.post("/onboarding/start")
async def start_session(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Starts a new onboarding session for the current user.
    If an active session already exists, returns the existing one.
    """
    # Check for existing active session
    # (Using hasattr check just in case the real model isn't hooked up yet)
    if hasattr(OnboardingSession, 'user_id'):
        existing_session = db.query(OnboardingSession).filter(
            OnboardingSession.user_id == str(current_user.id),
            OnboardingSession.status == "in_progress"
        ).first()
        
        if existing_session:
            return {
                "session_id": str(existing_session.id),
                "message": "Hi! I'm O.N.E — your Onboarding Navigation Environment. "
                           "I'm here to guide you through your first days at the company. "
                           "Let's start with the basics — what's your full name and email address?"
            }

    # Generate a unique ID (if model uses string IDs or just omit if auto-increment)
    new_session_id = str(uuid.uuid4())
    
    # Create a new session object
    new_session = OnboardingSession(
        id=new_session_id,
        user_id=str(current_user.id),
        status="in_progress",
        current_fsm_state="WELCOME",
        started_at=datetime.utcnow()
    )
    
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    
    return {
        "session_id": str(new_session.id),
        "message": "Hi! I'm O.N.E — your Onboarding Navigation Environment. "
                   "I'm here to guide you through your first days at the company. "
                   "Let's start with the basics — what's your full name and email address?"
    }

@router.get("/onboarding/{session_id}")
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
        
    # Using dictionary format or response schema, returning as a dict fallback due to dynamic properties
    return {
        "id": getattr(session_obj, "id", None),
        "user_id": getattr(session_obj, "user_id", None),
        "persona": getattr(session_obj, "persona", None),
        "status": getattr(session_obj, "status", None),
        "current_fsm_state": getattr(session_obj, "current_fsm_state", None)
    }

@router.get("/onboarding/{session_id}/progress")
async def get_progress(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Retrieve onboarding checklist progress summary for a given session.
    """
    # Assuming the specific user-session auth context is verified here similar to above
    # or inside the service itself. Let's do a basic check here if OnboardingSession is accessible:
    session_obj = db.query(OnboardingSession).filter(OnboardingSession.id == session_id).first()
    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found")
        
    if str(session_obj.user_id) != str(current_user.id) and current_user.role != "hr_admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    checklist_service = ChecklistService(db)
    progress_dict = await checklist_service.get_progress(session_id)
    
    return progress_dict
