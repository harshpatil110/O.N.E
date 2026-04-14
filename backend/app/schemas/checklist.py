from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class ChecklistItemResponse(BaseModel):
    """Schema for a single checklist item returned by the API."""
    id: UUID
    session_id: UUID
    item_key: str
    title: str
    description: Optional[str] = None
    category: str  # Free-form string from DB (e.g. "General", "Access", "Tooling")
    required: bool
    sort_order: int
    status: str  # Free-form string from DB (e.g. "pending", "completed", "skipped")
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class UpdateChecklistRequest(BaseModel):
    """Schema for updating a checklist item's status."""
    status: str
    notes: Optional[str] = None
