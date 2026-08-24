from langchain_core.tools import tool
from app.core.database import SessionLocal
from app.core.task_manager import get_next_task
from app.models.user import User
from app.models.tasks import RoleTask
from app.models.conversation_log import ConversationLog
from app.models.onboarding_session import OnboardingSession
from app.models.completed_verify_task import CompletedVerifyTask
from datetime import datetime
import re
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
    
    db = SessionLocal()
    try:
        # 1. Enforce State Machine: Find the active task
        from app.models.developer_task_state import DeveloperTaskState
        
        active_task = db.query(DeveloperTaskState).filter(
            DeveloperTaskState.user_id == user_id,
            DeveloperTaskState.status == 'active'
        ).first()
        
        if not active_task:
            return "Task submission failed: You currently have no 'active' task. It may already be pending admin verification, or all tasks are completed."

        task_name = active_task.task_name
        current_seq = active_task.task_sequence_number
        print(f"✅ Active task found: '{task_name}' (Seq: {current_seq})")

        # 2. Strict Timestamp Chat Isolation
        # Find exactly when this task started by looking at when the previous task was verified.
        previous_task = db.query(DeveloperTaskState).filter(
            DeveloperTaskState.user_id == user_id,
            DeveloperTaskState.task_sequence_number == current_seq - 1
        ).first()
        
        # If there is a previous task, use its updated_at timestamp as the lower bound.
        # (updated_at is set when a task transitions to 'verified')
        start_time = previous_task.updated_at if (previous_task and previous_task.updated_at) else datetime.min
        print(f"📅 Timestamp lower bound: {start_time}")

        # Fetch strictly bounded logs via the session
        session = db.query(OnboardingSession).filter(OnboardingSession.user_id == user_id).first()
        chat_history_text = ""
        if session:
            task_specific_logs = db.query(ConversationLog).filter(
                ConversationLog.session_id == session.id,
                ConversationLog.created_at >= start_time
            ).order_by(ConversationLog.created_at.asc()).all()
            
            print(f"📄 Isolated {len(task_specific_logs)} chat logs specifically for this task via Timestamp bounding.")
            
            chat_history_text = "\n".join([f"{log.role}: {log.content}" for log in task_specific_logs])
        
        if not chat_history_text.strip():
            chat_history_text = "[No conversation history recorded for this specific task timeframe.]"

        # 3. Anti-Hallucination XML Prompting
        print("🧠 Running AI Assessment with Strict Anti-Hallucination bounds...")
        eval_sys_prompt = """You are an engineering manager evaluating a developer's task completion based strictly on their chat history.
        CRITICAL INSTRUCTIONS:
        1. You MUST format your response using EXACTLY these XML tags: <speed>, <learning>, and <mistakes>.
        2. If the chat history is empty, or if the developer only said things like "mark this as done" without asking any questions, YOU MUST NOT invent an evaluation. 
        3. If there is insufficient data, output exactly this phrase inside the tags: "Insufficient chat data for analysis."

        Example of insufficient data response:
        <speed>Insufficient chat data for analysis.</speed>
        <learning>Insufficient chat data for analysis.</learning>
        <mistakes>Insufficient chat data for analysis.</mistakes>
        """
        
        eval_human_prompt = f"Task: {task_name}\nHistory:\n{chat_history_text}\n\nEvaluate using the XML tags."
        
        try:
            response = evaluator_llm.invoke([
                SystemMessage(content=eval_sys_prompt),
                HumanMessage(content=eval_human_prompt)
            ])
            response_text = response.content if hasattr(response, 'content') else str(response)
        except Exception as eval_err:
            print(f"⚠️ Evaluator LLM failed: {eval_err}. Using defaults.")
            response_text = ""
        
        # 4. Bulletproof Regex Extraction
        speed_match = re.search(r'<speed>(.*?)</speed>', response_text, re.DOTALL | re.IGNORECASE)
        learning_match = re.search(r'<learning>(.*?)</learning>', response_text, re.DOTALL | re.IGNORECASE)
        mistakes_match = re.search(r'<mistakes>(.*?)</mistakes>', response_text, re.DOTALL | re.IGNORECASE)
        
        # Safe fallbacks
        speed = speed_match.group(1).strip() if speed_match else "Insufficient chat data for analysis."
        learning = learning_match.group(1).strip() if learning_match else "Insufficient chat data for analysis."
        mistakes = mistakes_match.group(1).strip() if mistakes_match else "Insufficient chat data for analysis."

        # 5. Update State Machine & Commit
        active_task.status = 'pending_verification'
        active_task.speed_analysis = speed
        active_task.learning_curve = learning
        active_task.mistakes_made = mistakes
        active_task.updated_at = datetime.utcnow()
        print(f"💾 State transition: active -> pending_verification for '{task_name}'")

        if session:
            sys_log = ConversationLog(
                session_id=session.id, role='system',
                content=f"System: Chat submission successful. Task '{task_name}' is pending Admin Verification.",
                created_at=datetime.utcnow()
            )
            db.add(sys_log)
        
        db.commit()
        print("✅ SUCCESS: Evaluated and submitted to admin dashboard.")
        return f"Successfully submitted '{task_name}' for Admin verification. The status is now pending."
        
    except Exception as e:
        db.rollback()
        print(f"❌ CRITICAL TOOL ERROR: {e}")
        return f"Database error during submission: {str(e)}"
    finally:
        db.close()
        print("--- 🏁 TOOL EXECUTION FINISHED ---\n")

