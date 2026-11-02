from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from app.core.database import Base


class CompletedChecklistItem(Base):
    __tablename__ = "completed_checklist_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    task_id = Column(Integer, index=True, nullable=False)
    user_email = Column(String(255), index=True, nullable=False)
    subtask_number = Column(Integer, nullable=False)
    subtask_title = Column(String(255), nullable=False)
    verification_tier = Column(String(100), nullable=False)
    weight_score = Column(Integer, nullable=False, default=90)
    proof_type = Column(String(50), nullable=False, default="self_attestation")
    proof_text = Column(Text, nullable=True)
    screenshot_data = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "task_id": self.task_id,
            "user_email": self.user_email,
            "subtask_number": self.subtask_number,
            "subtask_title": self.subtask_title,
            "verification_tier": self.verification_tier,
            "weight_score": self.weight_score,
            "proof_type": self.proof_type,
            "proof_text": self.proof_text,
            "screenshot_data": self.screenshot_data,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<CompletedChecklistItem task_id={self.task_id} subtask={self.subtask_number} tier={self.verification_tier}>"

