from app.core.database import SessionLocal
from app.models.user import User
from app.models.developer_task_state import DeveloperTaskState
from app.api.tasks import initialize_tasks_for_user

def force_restore():
    db = SessionLocal()
    try:
        user_id = "d32c1e2d-8976-4a0b-8464-9abfeeebbb14"
        completed_count = 14
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            print("User not found.")
            return
            
        initialize_tasks_for_user(db, user)
        
        tasks = db.query(DeveloperTaskState).filter(
            DeveloperTaskState.user_id == user.id
        ).order_by(DeveloperTaskState.task_sequence_number.asc()).all()
        
        for idx, task in enumerate(tasks):
            if idx < completed_count:
                task.status = 'verified'
            elif idx == completed_count:
                task.status = 'active'
            else:
                task.status = 'locked'
        
        user.tasks_completed = completed_count
        user.onboarding_progress = min(100, int((completed_count / max(len(tasks), 1)) * 100))
        
        db.commit()
        print(f"✅ Success! Restored {user.email} to task #{completed_count + 1} (task name: {tasks[completed_count].task_name})")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    force_restore()
