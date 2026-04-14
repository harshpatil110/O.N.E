from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime
from app.schemas.checklist import ChecklistItemResponse

class SessionStartResponse(BaseModel):
    """Response when a new onboarding session is initialized."""
    session_id: str
    message: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "session_id": "sess-123",
                "message": "Hi! I'm O.N.E... Let's start with the basics."
            }
        }
    )

class SessionDetailResponse(BaseModel):
    """Detailed view of an onboarding session."""
    id: str
    user_id: str
    persona: Optional[Dict[str, Any]] = None
    status: str
    current_fsm_state: Optional[str] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "sess-123",
                "user_id": "user-456",
                "status": "in_progress",
                "current_fsm_state": "PLAN_GENERATION"
            }
        }
    )

class SessionProgressResponse(BaseModel):
    """Summary of onboarding progress."""
    total_items: int
    completed_count: int
    pending: int
    skipped: int
    percent_complete: float
    items: List[ChecklistItemResponse]
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_items": 10,
                "completed_count": 3,
                "percent_complete": 30.0
            }
        }
    )
