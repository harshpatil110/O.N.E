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


class ChatHistoryMessage(BaseModel):
    """A single message entry in the audit trail."""
    role: str
    content: str
    timestamp: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "role": "user",
                "content": "Hi, I'm starting my onboarding.",
                "timestamp": "2024-03-24T10:05:00+00:00"
            }
        }
    )


class SessionChatHistory(BaseModel):
    """Full audit trail for a specific onboarding session."""
    session_id: str
    employee_name: str
    employee_email: str
    status: str
    messages: List[ChatHistoryMessage]
    total_messages: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "employee_name": "Rahul Sharma",
                "employee_email": "rahul@test.com",
                "status": "in_progress",
                "messages": [
                    {"role": "user", "content": "Hi!", "timestamp": "2024-03-24T10:05:00+00:00"},
                    {"role": "assistant", "content": "Welcome!", "timestamp": "2024-03-24T10:05:01+00:00"}
                ],
                "total_messages": 2
            }
        }
    )


class AdminProfileResponse(BaseModel):
    """Response schema for admin profile data."""
    id: str
    name: str
    email: str
    role: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Alex Chen",
                "email": "alex@one-corp.com",
                "role": "hr_admin"
            }
        }
    )


class AdminProfileUpdate(BaseModel):
    """Request schema for updating admin profile."""
    name: Optional[str] = None
    email: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Alex Chen",
                "email": "alex@one-corp.com"
            }
        }
    )


