import uuid
from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID, ARRAY

from app.core.database import Base


class ChecklistTemplate(Base):
    __tablename__ = "checklist_templates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    item_key = Column(String(255), unique=True, index=True, nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(String, nullable=True)
    category = Column(String(100), nullable=False)
    required = Column(Boolean, default=True, nullable=False)
    sort_order = Column(Integer, nullable=False)
    applicable_roles = Column(ARRAY(String), nullable=True)
    applicable_levels = Column(ARRAY(String), nullable=True)
    applicable_stacks = Column(ARRAY(String), nullable=True)
    knowledge_base_refs = Column(ARRAY(String), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<ChecklistTemplate {self.item_key}>"
