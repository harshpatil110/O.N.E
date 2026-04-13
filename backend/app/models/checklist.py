from sqlalchemy import Column, String, Integer, Boolean, JSON, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ChecklistTemplate(Base):
    __tablename__ = "checklist_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    item_key = Column(String, unique=True, index=True)
    title = Column(String)
    description = Column(String)
    category = Column(String)
    required = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    applicable_roles = Column(JSON)  # List[str]
    applicable_levels = Column(JSON) # List[str]
    applicable_stacks = Column(JSON) # List[str]
    knowledge_base_refs = Column(JSON, nullable=True) # List[str]

class ChecklistItem(Base):
    __tablename__ = "checklist_items"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    item_key = Column(String)
    title = Column(String)
    description = Column(String)
    category = Column(String)
    required = Column(Boolean, default=True)
    sort_order = Column(Integer)
    applicable_roles = Column(JSON)
    applicable_levels = Column(JSON)
    applicable_stacks = Column(JSON)
    knowledge_base_refs = Column(JSON, nullable=True)
    status = Column(String, default="pending")  # "pending", "in_progress", "completed", "skipped"
    notes = Column(String, nullable=True)
    completed_at = Column(DateTime, nullable=True)
