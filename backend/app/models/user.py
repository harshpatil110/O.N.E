import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Boolean, Integer, Float
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="employee", nullable=False)
    department_role = Column(String(100), nullable=True)
    tasks_completed = Column(Integer, default=0, nullable=False)
    onboarding_progress = Column(Float, default=0.0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"
