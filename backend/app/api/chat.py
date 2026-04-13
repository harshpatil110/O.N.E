from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from backend.app.agents.orchestrator import AgentOrchestrator

router = APIRouter()

# --- Mock Dependencies ---
# These should be replaced with actual implementations from your project

def get_db():
    """Dependency to yield DB session"""
    # Yield a mock Session or real Session instance
    db = Session()
    try:
        yield db
    finally:
        db.close()

class User(BaseModel):
    id: str
    username: str

def get_current_user():
    """Dependency to get current authenticated user"""
    return User(id="user_123", username="developer")

class ChatMessageRequest(BaseModel):
    message: str

class ChatMessageResponse(BaseModel):
    reply: str
    session_id: str

# --- End Mock Dependencies ---

@router.post("/chat/{session_id}/message", response_model=ChatMessageResponse)
async def send_message(
    session_id: str,
    request: ChatMessageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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
