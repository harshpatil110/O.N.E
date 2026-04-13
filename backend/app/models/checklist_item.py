import uuid
from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY

from app.core.database import Base


class ChecklistItem(Base):
    __tablename__ = "checklist_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("onboarding_sessions.id", ondelete="CASCADE"), nullable=False)
    item_key = Column(String(255), nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(String, nullable=True)
    category = Column(String(100), nullable=False)
    required = Column(Boolean, default=True, nullable=False)
    sort_order = Column(Integer, nullable=False)
    applicable_roles = Column(ARRAY(String), nullable=True)
    applicable_levels = Column(ARRAY(String), nullable=True)
    applicable_stacks = Column(ARRAY(String), nullable=True)
    knowledge_base_refs = Column(ARRAY(String), nullable=True)
    status = Column(String(50), default="pending", nullable=False)
    completed_at = Column(DateTime, nullable=True)
    notes = Column(String, nullable=True)

    def __repr__(self):
        return f"<ChecklistItem {self.item_key} status={self.status}>"
