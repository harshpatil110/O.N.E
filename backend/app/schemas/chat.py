from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ConversationRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ChatMessageRequest(BaseModel):
    content: str
    metadata: Optional[Dict[str, Any]] = None

class ChatMessageResponse(BaseModel):
    id: str
    session_id: str
    role: ConversationRole
    content: str
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class MessageResponse(BaseModel):
    role: str
    content: str
    created_at: datetime

class ConversationHistoryResponse(BaseModel):
    session_id: str
    messages: list[MessageResponse]
