from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from app.core.database import Base


class DeveloperTaskState(Base):
    __tablename__ = "developer_task_states"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    task_sequence_number = Column(Integer, nullable=False)
    task_name = Column(String, nullable=False)

    # Strict state machine: locked -> active -> pending_verification -> verified
    status = Column(String(30), nullable=False, default="locked")

    # AI Evaluator columns (populated when status transitions to pending_verification)
    speed_analysis = Column(Text, nullable=True)
    learning_curve = Column(Text, nullable=True)
    mistakes_made = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<DeveloperTaskState user={self.user_id} seq={self.task_sequence_number} status={self.status}>"
