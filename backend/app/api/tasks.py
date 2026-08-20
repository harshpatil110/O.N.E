from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from app.core.database import get_db
from app.models.user import User
from app.models.tasks import RoleTask
from app.models.completed_verify_task import CompletedVerifyTask

router = APIRouter()

class CompleteTaskRequest(BaseModel):
    user_id: str

@router.get("/tasks/{user_id}")
def get_user_tasks(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    role = user.department_role
    if not role:
        raise HTTPException(status_code=404, detail="User role not found")
        
    role_record = db.query(RoleTask).filter(RoleTask.department_role == role).first()
    if not role_record or not role_record.tasks:
        raise HTTPException(status_code=404, detail="Tasks for role not found")
        
    return {
        "role": role,
        "tasks_completed": user.tasks_completed or 0,
        "progress_percentage": user.onboarding_progress or 0,
        "tasks_array": role_record.tasks
    }

@router.post("/tasks/complete")
def complete_user_task(req: CompleteTaskRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == req.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    role = user.department_role
    role_record = db.query(RoleTask).filter(RoleTask.department_role == role).first()
    if not role_record:
        raise HTTPException(status_code=404, detail="Role tasks not found")
        
    total_tasks = len(role_record.tasks) if role_record.tasks else 20
    current_completed = user.tasks_completed or 0
    
    if current_completed < total_tasks:
        user.tasks_completed = current_completed + 1
        user.onboarding_progress = min(100, int((user.tasks_completed / total_tasks) * 100))
        db.commit()
        db.refresh(user)
        
    return {
        "tasks_completed": user.tasks_completed,
        "progress_percentage": user.onboarding_progress
    }

@router.get("/my-task-statuses/{user_id}")
def get_my_task_statuses(user_id: str, db: Session = Depends(get_db)):
    """Fetches the verification status of tasks submitted by the given developer."""
    try:
        tasks = db.query(CompletedVerifyTask).filter(CompletedVerifyTask.user_id == user_id).all()
        
        status_map = {}
        for task in tasks:
            status_map[task.task_name] = "verified" if task.is_verified else "pending"
            
        return {"status": "success", "task_statuses": status_map}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
