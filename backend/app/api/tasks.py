from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from app.core.database import get_db
from app.models.user import User
from app.models.tasks import RoleTask
from app.models.developer_task_state import DeveloperTaskState
from app.models.conversation_log import ConversationLog
from app.models.onboarding_session import OnboardingSession
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from datetime import datetime

router = APIRouter()

evaluator_llm = ChatOllama(model="qwen2.5:3b", temperature=0.1)


# ─── Pydantic Models ───────────────────────────────────────────────

class TaskSubmitRequest(BaseModel):
    task_id: int


# ─── Task Initialization ───────────────────────────────────────────

def initialize_tasks_for_user(db: Session, user: User):
    """Populates DeveloperTaskState rows for a user from their RoleTask template.
    Task 1 = 'active', Tasks 2-N = 'locked'. Idempotent — skips if rows exist."""
    existing = db.query(DeveloperTaskState).filter(
        DeveloperTaskState.user_id == user.id
    ).first()
    if existing:
        return  # Already initialized

    role_record = db.query(RoleTask).filter(
        RoleTask.department_role == user.department_role
    ).first()
    if not role_record or not role_record.tasks:
        return

    for idx, task_name in enumerate(role_record.tasks):
        state = DeveloperTaskState(
            user_id=user.id,
            task_sequence_number=idx + 1,
            task_name=task_name,
            status="active" if idx == 0 else "locked"
        )
        db.add(state)
    db.commit()
    print(f"✅ Initialized {len(role_record.tasks)} tasks for user {user.email}")


# ─── GET /tasks/states/{user_id} — Full task array for the developer UI ─────

@router.get("/tasks/states/{user_id}")
def get_task_states(user_id: str, db: Session = Depends(get_db)):
    """Returns the complete ordered task list with DB-driven statuses."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Auto-initialize if this user has no task states yet
    initialize_tasks_for_user(db, user)

    tasks = db.query(DeveloperTaskState).filter(
        DeveloperTaskState.user_id == user.id
    ).order_by(DeveloperTaskState.task_sequence_number.asc()).all()

    return {
        "status": "success",
        "role": user.department_role,
        "tasks": [
            {
                "id": t.id,
                "sequence": t.task_sequence_number,
                "task_name": t.task_name,
                "status": t.status
            }
            for t in tasks
        ]
    }


# ─── POST /tasks/submit — Developer submits active task for verification ─────

@router.post("/tasks/submit")
def submit_task_for_verification(req: TaskSubmitRequest, db: Session = Depends(get_db)):
    """Transitions active task -> pending_verification with AI evaluation."""
    print(f"\n--- 📤 TASK SUBMIT: task_id={req.task_id} ---")

    task = db.query(DeveloperTaskState).filter(
        DeveloperTaskState.id == req.task_id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Guard: task must be 'active' to submit
    if task.status != "active":
        raise HTTPException(
            status_code=400,
            detail=f"Task is '{task.status}', not 'active'. Cannot submit."
        )

    # Guard: no other task for this user can be pending
    already_pending = db.query(DeveloperTaskState).filter(
        DeveloperTaskState.user_id == task.user_id,
        DeveloperTaskState.status == "pending_verification"
    ).first()
    if already_pending:
        raise HTTPException(
            status_code=400,
            detail="You already have a task pending admin review. Wait for approval."
        )

    # Fetch chat history for AI evaluation
    user = db.query(User).filter(User.id == task.user_id).first()
    session = db.query(OnboardingSession).filter(
        OnboardingSession.user_id == task.user_id
    ).first()

    speed = "Completed task within expected timeframe."
    learning = "Standard learning progression observed."
    mistakes = "No critical mistakes logged."

    if session:
        recent_logs = db.query(ConversationLog).filter(
            ConversationLog.session_id == session.id
        ).order_by(ConversationLog.created_at.desc()).limit(10).all()
        recent_logs.reverse()
        chat_text = "\n".join([f"{l.role}: {l.content}" for l in recent_logs])
        print(f"📝 Found {len(recent_logs)} logs for evaluation.")

        try:
            print("🧠 Running AI Assessment...")
            response = evaluator_llm.invoke([
                SystemMessage(content="""You are an engineering manager evaluating a developer's task completion.
                Return exactly 3 sections separated by '|':
                1. Speed Analysis  2. Learning Curve  3. Mistakes Made
                Keep each to 1 sentence."""),
                HumanMessage(content=f"Task: {task.task_name}\nHistory:\n{chat_text}\n\nEvaluate: Speed|Learning|Mistakes")
            ])
            parts = (response.content if hasattr(response, 'content') else str(response)).split('|')
            if len(parts) > 0: speed = parts[0].strip()
            if len(parts) > 1: learning = parts[1].strip()
            if len(parts) > 2: mistakes = parts[2].strip()
            print(f"✅ AI eval done: {len(parts)} parts")
        except Exception as e:
            print(f"⚠️ LLM failed (using defaults): {e}")

    # Transition: active -> pending_verification
    task.status = "pending_verification"
    task.speed_analysis = speed
    task.learning_curve = learning
    task.mistakes_made = mistakes
    task.updated_at = datetime.utcnow()

    # Inject system notification
    if session:
        db.add(ConversationLog(
            session_id=session.id, role='system',
            content=f"System: Task '{task.task_name}' submitted for Admin Verification. Awaiting approval.",
            created_at=datetime.utcnow()
        ))

    db.commit()
    print(f"✅ Task #{task.task_sequence_number} -> pending_verification")
    return {"status": "success", "message": f"Task '{task.task_name}' submitted for verification."}
