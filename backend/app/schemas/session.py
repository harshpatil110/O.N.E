from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from datetime import datetime
from enum import Enum

class SessionStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"

class SessionResponse(BaseModel):
    id: str
    user_id: str
    persona: Optional[dict[str, Any]] = None
    status: SessionStatus
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
