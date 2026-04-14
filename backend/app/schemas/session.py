from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from datetime import datetime
from uuid import UUID


class SessionResponse(BaseModel):
    """Schema for a full onboarding session record."""
    id: UUID
    user_id: UUID
    persona: Optional[dict[str, Any]] = None
    status: str
    current_fsm_state: Optional[str] = None
    current_checklist_index: int = 0
    started_at: datetime
    completed_at: Optional[datetime] = None
    hr_notified: bool = False

    model_config = ConfigDict(from_attributes=True)

class StartSessionRequest(BaseModel):
    user_id: str

class ProgressResponse(BaseModel):
    completed_items: int
    total_items: int
    percentage: float

class SessionStatus:
    """Constants for session status values (non-Enum for flexible matching)."""
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"
