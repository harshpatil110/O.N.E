from typing import Union
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.tasks import RoleTask


from app.models.developer_task_state import DeveloperTaskState

def get_next_task(db: Session, user_id: Union[UUID, str]) -> str:
    """
    Fetch the user's current active task directly from the DeveloperTaskState ledger.
    """
    if isinstance(user_id, str):
        try:
            user_id = UUID(user_id)
        except ValueError:
            return "Invalid user ID format."

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return "User not found."

    # Try to find the active task first
    active_task = db.query(DeveloperTaskState).filter(
        DeveloperTaskState.user_id == user.id,
        DeveloperTaskState.status == "active"
    ).first()
    
    if active_task:
        return active_task.task_name
        
    # If no active task, check if one is pending
    pending_task = db.query(DeveloperTaskState).filter(
        DeveloperTaskState.user_id == user.id,
        DeveloperTaskState.status == "pending_verification"
    ).first()
    
    if pending_task:
        return f"{pending_task.task_name} (Currently Pending Admin Verification)"

    # If no active or pending tasks, check if initialized
    total_tasks = db.query(DeveloperTaskState).filter(
        DeveloperTaskState.user_id == user.id
    ).count()
    
    if total_tasks == 0:
        return f"No tasks initialized yet for role '{user.department_role}'."

    return "All onboarding tasks completed!"
