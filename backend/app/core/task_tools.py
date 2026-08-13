from langchain_core.tools import tool
from app.core.database import SessionLocal
from app.core.task_manager import get_next_task
from app.models.user import User
from app.models.tasks import RoleTask

@tool("get_current_task")
def get_current_task(user_id: str) -> str:
    """Use this tool when a user asks what their next task is, what they need to work on, 
    or what their current onboarding step is.
    Input MUST be the user's UUID string."""
    try:
        with SessionLocal() as db:
            task_str = get_next_task(db, user_id)
            user = db.query(User).filter(User.id == user_id).first()
            n = (user.tasks_completed or 0) + 1 if user else 1
            return f"Task [{n}]: {task_str}"
    except Exception as e:
        return f"Error fetching current task: {str(e)}"

@tool("mark_task_complete")
def mark_task_complete(user_id: str) -> str:
    """Use this tool when a user explicitly states they finished, completed, or did their 
    current task (e.g., 'I completed task 1', 'Mark as done', 'Finished it').
    Input MUST be the user's UUID string."""
    try:
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return "User not found."
            
            department_role = user.department_role
            if not department_role:
                return "User has no assigned department role."

            role_task_record = db.query(RoleTask).filter(RoleTask.department_role == department_role).first()
            if not role_task_record or not role_task_record.tasks:
                return "No onboarding tasklist found."
                
            total_tasks = len(role_task_record.tasks)
            current_completed = user.tasks_completed or 0
            
            if current_completed >= total_tasks:
                return "All onboarding tasks are already completed!"
                
            user.tasks_completed = current_completed + 1
            user.onboarding_progress = min(100, int((user.tasks_completed / total_tasks) * 100))
            db.commit()
            
            next_task = get_next_task(db, user_id)
            return f"Great job! Task marked complete. Progress updated to {user.onboarding_progress}%. Your next task is: {next_task}"
    except Exception as e:
        return f"Error marking task complete: {str(e)}"
