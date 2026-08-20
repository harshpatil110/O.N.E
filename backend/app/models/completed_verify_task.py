from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from app.core.database import Base

class CompletedVerifyTask(Base):
    __tablename__ = "completed_verify_tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    task_name = Column(String, nullable=False)
    
    # AI Generated Insights
    speed_analysis = Column(Text, nullable=True)
    learning_curve = Column(Text, nullable=True)
    mistakes_made = Column(Text, nullable=True)
    
    # State Management
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    verified_at = Column(DateTime, nullable=True)
