from uuid import UUID
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class SessionSummary(BaseModel):
    session_id: UUID
    employee_name: str
    employee_email: str
    role: str
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    percent_complete: int

    class Config:
        from_attributes = True

class PaginatedSessions(BaseModel):
    items: List[SessionSummary]
    total: int
    page: int
    page_size: int

class AdminMetrics(BaseModel):
    total_sessions: int
    active_sessions: int
    completed_sessions: int
    completion_rate: float
    avg_duration_hours: float
    completions_this_week: int
