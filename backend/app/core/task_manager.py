from typing import Union
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.tasks import RoleTask


def get_next_task(db: Session, user_id: Union[UUID, str]) -> str:
    """
    Fetch the user's next sequential onboarding task based on their 
    department_role and tasks_completed integer index.
    """
    if isinstance(user_id, str):
        try:
            user_id = UUID(user_id)
        except ValueError:
            return "Invalid user ID format."

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return "User not found."

    department_role = user.department_role
    if not department_role:
        return "User has no assigned department role."

    tasks_completed = user.tasks_completed or 0

    role_task_record = (
        db.query(RoleTask)
        .filter(RoleTask.department_role == department_role)
        .first()
    )
    if not role_task_record or not role_task_record.tasks:
        return f"No onboarding tasklist found for role '{department_role}'."

    tasks = role_task_record.tasks

    if tasks_completed >= len(tasks):
        return "All onboarding tasks completed!"

    if tasks_completed < 0:
        tasks_completed = 0

    return tasks[tasks_completed]
