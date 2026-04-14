from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ConversationRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ChatMessageRequest(BaseModel):
    """Schema for an incoming chat message."""
    message: str
    metadata: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Hi, I'm Rahul. I'm a senior backend developer working with Python.",
            }
        }
    )

class ChatMessageResponse(BaseModel):
    """Schema for the assistant's reply."""
    reply: str
    session_id: str
    metadata: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "reply": "Welcome Rahul! I've set up your onboarding checklist based on your profile.",
                "session_id": "sess_456"
            }
        }
    )

class MessageResponse(BaseModel):
    role: str
    content: str
    created_at: datetime

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "role": "user",
                "content": "What is the policy for GitHub access?",
                "created_at": "2024-03-24T12:05:00Z"
            }
        }
    )

class ConversationHistoryResponse(BaseModel):
    session_id: str
    messages: list[MessageResponse]
