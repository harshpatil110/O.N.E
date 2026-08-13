import uuid
from sqlalchemy import Column, String, JSON
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class RoleTask(Base):
    __tablename__ = "role_tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    department_role = Column(String(100), unique=True, index=True, nullable=False)
    tasks = Column(JSON, nullable=False)

    def __repr__(self):
        return f"<RoleTask {self.department_role}>"
