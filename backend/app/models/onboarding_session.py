import uuid
from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.core.database import Base


class OnboardingSession(Base):
    __tablename__ = "onboarding_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    persona = Column(JSONB, nullable=True)
    status = Column(String(50), default="in_progress", nullable=False)
    current_fsm_state = Column(String(255), nullable=True)
    current_checklist_index = Column(Integer, default=0, nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    hr_notified = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<OnboardingSession {self.id} status={self.status}>"
