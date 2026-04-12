from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ItemCategory(str, Enum):
    ACCESS = "access"
    TOOLING = "tooling"
    DOCUMENTATION = "documentation"
    COMPLIANCE = "compliance"
    TEAM = "team"

class ItemStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"

class ChecklistItemResponse(BaseModel):
    id: str
    session_id: str
    item_key: str
    title: str
    description: Optional[str] = None
    category: ItemCategory
    required: bool
    sort_order: int
    status: ItemStatus
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class UpdateChecklistRequest(BaseModel):
    status: ItemStatus
