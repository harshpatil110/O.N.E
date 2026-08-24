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
def mark_task_complete(user_id: str) -> str:
    """Use this tool STRICTLY AND ONLY WHEN the user explicitly states they have finished their assigned task."""
    print(f"\n--- 🛠️ AI TOOL TRIGGERED: mark_task_complete via Chat ---")
    print(f"User ID: {user_id}")
    
    db = SessionLocal()
    try:
        # 1. Enforce State Machine: Find the EXACT active task from DB
        from app.models.developer_task_state import DeveloperTaskState
        
        active_task = db.query(DeveloperTaskState).filter(
            DeveloperTaskState.user_id == user_id,
            DeveloperTaskState.status == 'active'
        ).first()
        
        if not active_task:
            print("❌ No active task found for this user.")
            return "Task submission failed: You currently have no 'active' task. It may already be pending admin verification, or all tasks are completed."

        task_name = active_task.task_name
        print(f"✅ Active task found: '{task_name}' (seq #{active_task.task_sequence_number})")

        # 2. Fetch recent chat logs for AI evaluation
        session = db.query(OnboardingSession).filter(OnboardingSession.user_id == user_id).first()
        chat_history_text = ""
        if session:
            recent_logs = db.query(ConversationLog).filter(
                ConversationLog.session_id == session.id
            ).order_by(ConversationLog.created_at.desc()).limit(10).all()
            recent_logs.reverse()
            chat_history_text = "\n".join([f"{log.role}: {log.content}" for log in recent_logs])
            print(f"📝 Found {len(recent_logs)} chat logs to evaluate.")

        # 3. Run AI Evaluation (Speed, Learning Curve, Mistakes)
        print("🧠 Running AI Assessment (Speed, Learning, Mistakes)...")
        eval_sys_prompt = """You are an engineering manager evaluating a developer's task completion based on their chat history. 
        Analyze the history and return exactly 3 sections separated by the pipe '|' character:
        1. Speed Analysis
        2. Learning Curve
        3. Mistakes Made
        Keep each section to 1 sentence."""
        
        eval_human_prompt = f"Task: {task_name}\nHistory:\n{chat_history_text}\n\nEvaluate using format: Speed|Learning|Mistakes"
        
        try:
            response = evaluator_llm.invoke([
                SystemMessage(content=eval_sys_prompt),
                HumanMessage(content=eval_human_prompt)
            ])
            response_text = response.content if hasattr(response, 'content') else str(response)
            parts = response_text.split('|')
            print(f"✅ AI Evaluation Complete. Parts found: {len(parts)}")
            print(f"   Raw response: {response_text[:200]}")
        except Exception as eval_err:
            print(f"⚠️ Evaluator LLM failed: {eval_err}. Using defaults.")
            parts = []
        
        speed = parts[0].strip() if len(parts) > 0 else "Analysis completed rapidly."
        learning = parts[1].strip() if len(parts) > 1 else "Demonstrated standard comprehension."
        mistakes = parts[2].strip() if len(parts) > 2 else "No critical mistakes logged."

        # 4. Update the State Machine row: active -> pending_verification
        active_task.status = 'pending_verification'
        active_task.speed_analysis = speed
        active_task.learning_curve = learning
        active_task.mistakes_made = mistakes
        active_task.updated_at = datetime.utcnow()
        print(f"💾 State transition: active -> pending_verification for '{task_name}'")

        # 5. Log system notification in chat
        if session:
            sys_log = ConversationLog(
                session_id=session.id, role='system',
                content=f"System: Task '{task_name}' submitted for Admin Verification. You will be notified once approved.",
                created_at=datetime.utcnow()
            )
            db.add(sys_log)
        
        db.commit()
        print("✅ SUCCESS: Task submitted to admin dashboard via DeveloperTaskState.")
        return f"Successfully submitted '{task_name}' for Admin verification. The status is now 'pending_verification'. Tell the user to wait for approval."
        
    except Exception as e:
        db.rollback()
        print(f"❌ CRITICAL TOOL ERROR: {e}")
        return f"System error during task submission: {str(e)}"
    finally:
        db.close()
        print("--- 🏁 TOOL EXECUTION FINISHED ---\n")

