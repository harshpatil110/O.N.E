from pydantic import BaseModel, ConfigDict, field_serializer
from datetime import datetime
from typing import Optional, List, Any
from uuid import UUID

class SessionSummary(BaseModel):
    session_id: Any  # Accept UUID objects from SQLAlchemy
    employee_name: str
    employee_email: str
    role: str
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    percent_complete: int

    @field_serializer('session_id')
    def serialize_session_id(self, v):
        return str(v)

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "employee_name": "Rahul Sharma",
                "employee_email": "rahul@test.com",
                "role": "Backend Developer",
                "status": "in_progress",
                "started_at": "2024-03-24T10:00:00Z",
                "percent_complete": 45
            }
        }
    )

class PaginatedSessions(BaseModel):
    items: List[SessionSummary]
    total: int
    page: int
    page_size: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "items": [],
                "total": 10,
                "page": 1,
                "page_size": 10
            }
        }
    )

class AdminMetrics(BaseModel):
    total_sessions: int
    active_sessions: int
    completed_sessions: int
    completion_rate: float
    avg_duration_hours: float
    completions_this_week: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_sessions": 15,
                "active_sessions": 12,
                "completed_sessions": 3,
                "completion_rate": 20.0,
                "avg_duration_hours": 42.5,
                "completions_this_week": 2
            }
        }
    )
