from langchain_core.tools import tool
from app.core.database import SessionLocal
from app.core.task_manager import get_next_task
from app.models.user import User
from app.models.tasks import RoleTask
from app.models.conversation_log import ConversationLog
from app.models.onboarding_session import OnboardingSession
from app.models.completed_verify_task import CompletedVerifyTask
from datetime import datetime
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

evaluator_llm = ChatOllama(model="qwen2.5:3b", temperature=0.1)

@tool("get_current_task")
def get_current_task(user_id: str) -> str:
    """Use this tool ONLY to fetch and tell the user what their current assigned task is. 
    CRITICAL: DO NOT use this tool to mark a task as done. ONLY explain the task to the user."""
    try:
        with SessionLocal() as db:
            task_str = get_next_task(db, user_id)
            user = db.query(User).filter(User.id == user_id).first()
            n = (user.tasks_completed or 0) + 1 if user else 1
            return f"Task [{n}]: {task_str}"
    except Exception as e:
        return f"Error fetching current task: {str(e)}"

@tool("mark_task_complete")
def mark_task_complete(user_id: str, task_name: str) -> str:
    """Use this tool STRICTLY AND ONLY WHEN the user explicitly states they have finished their task. 
    You must provide the user_id and the exact task_name they completed."""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return "Error: User not found."

        session = db.query(OnboardingSession).filter(OnboardingSession.user_id == user.id).first()
        if not session:
            return "Error: User session not found."

        # 1. Fetch recent logs to evaluate performance
        recent_logs = db.query(ConversationLog).filter(
            ConversationLog.session_id == session.id
        ).order_by(ConversationLog.created_at.desc()).limit(15).all()
        recent_logs.reverse()
        
        chat_history_text = "\n".join([f"{log.role}: {log.content}" for log in recent_logs])

        # 2. Run the AI Assessment
        eval_sys_prompt = """You are an engineering manager evaluating a developer's task completion based on their chat history. 
        Analyze the history and return exactly 3 sections separated by the pipe '|' character:
        1. Speed Analysis (How fast/efficient were they?)
        2. Learning Curve (Did they understand concepts quickly?)
        3. Mistakes Made (What errors did they hit and resolve?)
        Keep each section to 2 sentences maximum."""
        
        eval_human_prompt = f"Task: {task_name}\nHistory:\n{chat_history_text}\n\nEvaluate them now using the format: Speed|Learning|Mistakes"
        
        response = evaluator_llm.invoke([
            SystemMessage(content=eval_sys_prompt),
            HumanMessage(content=eval_human_prompt)
        ])
        
        response_text = response.content if hasattr(response, 'content') else str(response)
        parts = response_text.split('|')
        
        speed = parts[0].strip() if len(parts) > 0 else "Analysis unavailable."
        learning = parts[1].strip() if len(parts) > 1 else "Analysis unavailable."
        mistakes = parts[2].strip() if len(parts) > 2 else "Analysis unavailable."

        # 3. Save to the Verification Table
        verify_record = CompletedVerifyTask(
            user_id=user.id,
            task_name=task_name,
            speed_analysis=speed,
            learning_curve=learning,
            mistakes_made=mistakes
        )
        db.add(verify_record)
        
        # 4. Notify the user via system log
        sys_log = ConversationLog(
            session_id=session.id, role='system',
            content=f"System: Task '{task_name}' submitted for Admin Verification. You will be notified once approved.",
            created_at=datetime.utcnow()
        )
        db.add(sys_log)
        
        db.commit()
        return f"Successfully submitted '{task_name}' for HR/Admin verification. Tell the user it is pending review."
        
    except Exception as e:
        db.rollback()
        return f"System error during task submission: {str(e)}"
    finally:
        db.close()
