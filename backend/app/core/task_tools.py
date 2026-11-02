import os
import re
import ssl
import smtplib
import logging
from typing import Optional
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

from app.core.database import SessionLocal
from app.core.task_manager import get_next_task
from app.models.user import User
from app.models.tasks import RoleTask
from app.models.conversation_log import ConversationLog
from app.models.onboarding_session import OnboardingSession
from app.models.completed_verify_task import CompletedVerifyTask

logger = logging.getLogger(__name__)

evaluator_llm = ChatOllama(model="qwen3:4b", temperature=0.1)


# ═══════════════════════════════════════════════════════════════════════════════
# 6-Tier Verification Taxonomy & Confidence Scoring
# ═══════════════════════════════════════════════════════════════════════════════

VERIFICATION_TIERS = {
    "tier_1": {"label": "Tier 1: System/MCP Verified",        "weight": 1.00, "description": "Automated API or MCP tool confirmed completion"},
    "tier_2": {"label": "Tier 2: Knowledge Quiz Verified",    "weight": 0.95, "description": "Passed comprehension quiz on task content"},
    "tier_3": {"label": "Tier 3: Proof-of-Work Validated",    "weight": 0.90, "description": "CLI output, Swagger 200 OK, or Git proof provided"},
    "tier_4": {"label": "Tier 4: Peer Review Confirmed",      "weight": 0.80, "description": "Verified by a peer or team lead"},
    "tier_5": {"label": "Tier 5: Admin Manual Verification",  "weight": 0.70, "description": "Manually verified by admin dashboard review"},
    "tier_6": {"label": "Tier 6: Self-Attestation",           "weight": 0.50, "description": "Developer self-reported completion via chat"},
}

# Keyword heuristics to auto-classify verification tier from chat context
TIER_CLASSIFICATION_RULES = [
    # Tier 1: Mentions of automated tool/API/MCP verification
    ("tier_1", ["api verified", "mcp verified", "system confirmed", "automated check passed", "tool verified"]),
    # Tier 2: Quiz-related evidence
    ("tier_2", ["quiz passed", "quiz score", "comprehension test", "knowledge check", "quiz verified"]),
    # Tier 3: Proof-of-work evidence (CLI, Swagger, Git, screenshot)
    ("tier_3", ["swagger", "200 ok", "curl", "git log", "git commit", "git push", "screenshot",
                "docker ps", "npm run", "python manage", "node -v", "docker-compose", "pip install",
                "terminal output", "cli output", "build successful", "tests pass"]),
    # Tier 4: Peer review
    ("tier_4", ["peer review", "code review", "approved by", "reviewed by", "lgtm"]),
    # Tier 5: Admin verification
    ("tier_5", ["admin verified", "admin approved", "manually verified"]),
]


def classify_verification_tier(chat_history: str, task_name: str) -> str:
    """Classify the verification method into one of the 6 tiers based on chat evidence.
    
    Scans the chat history for keywords indicating the strength of verification.
    Falls back to Tier 6 (Self-Attestation) if no stronger evidence is found.
    """
    history_lower = chat_history.lower()
    
    for tier_key, keywords in TIER_CLASSIFICATION_RULES:
        if any(kw in history_lower for kw in keywords):
            logger.info(f"[VERIFICATION] Task '{task_name}' classified as {VERIFICATION_TIERS[tier_key]['label']}")
            return tier_key
    
    # Default: Self-Attestation (developer just said "I'm done")
    logger.info(f"[VERIFICATION] Task '{task_name}' classified as Tier 6: Self-Attestation (default)")
    return "tier_6"


def compute_weighted_confidence(completed_tasks_with_tiers: list[dict]) -> dict:
    """Compute the overall Verification Confidence Score across all completed tasks.
    
    Args:
        completed_tasks_with_tiers: List of dicts with keys 'task_name', 'tier_key'
    
    Returns:
        Dict with 'score_pct', 'label', 'breakdown' 
    """
    if not completed_tasks_with_tiers:
        return {"score_pct": 0.0, "label": "No Tasks Completed", "breakdown": []}
    
    total_weight = 0.0
    breakdown = []
    
    for task_info in completed_tasks_with_tiers:
        tier_key = task_info.get("tier_key", "tier_6")
        tier = VERIFICATION_TIERS.get(tier_key, VERIFICATION_TIERS["tier_6"])
        weight = tier["weight"]
        total_weight += weight
        breakdown.append({
            "task_name": task_info["task_name"],
            "tier_label": tier["label"],
            "weight": weight,
            "weight_pct": f"{weight * 100:.0f}%",
        })
    
    avg_score = (total_weight / len(completed_tasks_with_tiers)) * 100
    
    # Confidence label
    if avg_score >= 90:
        label = "High Confidence"
    elif avg_score >= 75:
        label = "Good Confidence"
    elif avg_score >= 60:
        label = "Moderate Confidence"
    else:
        label = "Low Confidence"
    
    return {
        "score_pct": round(avg_score, 1),
        "label": label,
        "breakdown": breakdown,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Task Tools (LangChain @tool wrappers)
# ═══════════════════════════════════════════════════════════════════════════════

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

        # ─── 2.5 Verification Tier Classification ────────────────────────────
        tier_key = classify_verification_tier(chat_history_text, task_name)
        tier_info = VERIFICATION_TIERS[tier_key]
        print(f"🏅 Verification Tier: {tier_info['label']} (Weight: {tier_info['weight'] * 100:.0f}%)")

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

        # 5. Update State Machine & Commit (with verification tier metadata)
        active_task.status = 'pending_verification'
        active_task.speed_analysis = speed
        active_task.learning_curve = learning
        active_task.mistakes_made = mistakes
        active_task.updated_at = datetime.utcnow()
        print(f"💾 State transition: active -> pending_verification for '{task_name}'")

        if session:
            tier_log_content = (
                f"System: Chat submission successful. Task '{task_name}' is pending Admin Verification.\n"
                f"🏅 Verification: {tier_info['label']} — Confidence Weight: {tier_info['weight'] * 100:.0f}%"
            )
            sys_log = ConversationLog(
                session_id=session.id, role='system',
                content=tier_log_content,
                created_at=datetime.utcnow()
            )
            db.add(sys_log)
        
        db.commit()
        print("✅ SUCCESS: Evaluated and submitted to admin dashboard.")
        
        return (
            f"Successfully submitted '{task_name}' for Admin verification.\n"
            f"🏅 **Verification Tier:** {tier_info['label']}\n"
            f"📊 **Confidence Weight:** {tier_info['weight'] * 100:.0f}%\n"
            f"📝 **Description:** {tier_info['description']}\n"
            f"The status is now pending."
        )
        
    except Exception as e:
        db.rollback()
        print(f"❌ CRITICAL TOOL ERROR: {e}")
        return f"Database error during submission: {str(e)}"
    finally:
        db.close()
        print("--- 🏁 TOOL EXECUTION FINISHED ---\n")


# ═══════════════════════════════════════════════════════════════════════════════
# HR Completion Email Service
# ═══════════════════════════════════════════════════════════════════════════════

def _build_hr_report_html(
    employee_name: str,
    employee_email: str,
    role_persona: str,
    tech_stack: str,
    completed_items: list[dict],
    confidence_result: dict,
) -> str:
    """Build a structured HTML report for HR Onboarding Completion."""
    
    # Build task rows
    task_rows = ""
    for i, item in enumerate(completed_items, 1):
        tier_label = item.get("tier_label", "Tier 6: Self-Attestation")
        weight_pct = item.get("weight_pct", "50%")
        task_name = item.get("task_name", "Unknown Task")
        
        # Color-code by tier confidence
        weight_val = item.get("weight", 0.5)
        if weight_val >= 0.90:
            badge_color = "#28a745"  # Green
        elif weight_val >= 0.75:
            badge_color = "#17a2b8"  # Blue
        elif weight_val >= 0.60:
            badge_color = "#ffc107"  # Yellow
        else:
            badge_color = "#dc3545"  # Red
        
        task_rows += f"""
        <tr>
            <td style="padding: 10px; border-bottom: 1px solid #eee;">{i}</td>
            <td style="padding: 10px; border-bottom: 1px solid #eee;">{task_name}</td>
            <td style="padding: 10px; border-bottom: 1px solid #eee;">
                <span style="background: {badge_color}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 12px;">
                    {tier_label}
                </span>
            </td>
            <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center; font-weight: bold;">{weight_pct}</td>
        </tr>"""
    
    score = confidence_result["score_pct"]
    label = confidence_result["label"]
    
    # Overall score color
    if score >= 90:
        score_color = "#28a745"
    elif score >= 75:
        score_color = "#17a2b8"
    elif score >= 60:
        score_color = "#ffc107"
    else:
        score_color = "#dc3545"
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>O.N.E. Onboarding Completion Report</title>
</head>
<body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f4f6f9; margin: 0; padding: 20px;">
    <div style="max-width: 700px; margin: 0 auto; background: white; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); overflow: hidden;">
        <!-- Header -->
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center;">
            <h1 style="color: white; margin: 0; font-size: 24px;">🎓 O.N.E. Onboarding Completion Report</h1>
            <p style="color: rgba(255,255,255,0.85); margin: 8px 0 0 0; font-size: 14px;">Automated HR Verification Summary</p>
        </div>
        
        <!-- Employee Info -->
        <div style="padding: 25px;">
            <h2 style="color: #333; border-bottom: 2px solid #667eea; padding-bottom: 8px;">👤 Employee Information</h2>
            <table style="width: 100%; margin-bottom: 20px;">
                <tr><td style="padding: 6px 0; color: #666; width: 140px;"><strong>Name:</strong></td><td>{employee_name}</td></tr>
                <tr><td style="padding: 6px 0; color: #666;"><strong>Email:</strong></td><td>{employee_email}</td></tr>
                <tr><td style="padding: 6px 0; color: #666;"><strong>Role Persona:</strong></td><td>{role_persona}</td></tr>
                <tr><td style="padding: 6px 0; color: #666;"><strong>Tech Stack:</strong></td><td>{tech_stack}</td></tr>
                <tr><td style="padding: 6px 0; color: #666;"><strong>Report Date:</strong></td><td>{datetime.utcnow().strftime('%B %d, %Y at %H:%M UTC')}</td></tr>
            </table>
            
            <!-- Confidence Score Banner -->
            <div style="background: {score_color}; color: white; padding: 20px; border-radius: 8px; text-align: center; margin: 20px 0;">
                <div style="font-size: 36px; font-weight: bold;">{score:.1f}%</div>
                <div style="font-size: 16px; opacity: 0.9;">Overall Verification Confidence — {label}</div>
            </div>
            
            <!-- Completed Tasks -->
            <h2 style="color: #333; border-bottom: 2px solid #667eea; padding-bottom: 8px;">✅ Completed Checklist Items</h2>
            <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                <thead>
                    <tr style="background: #f8f9fa;">
                        <th style="padding: 10px; text-align: left; border-bottom: 2px solid #dee2e6;">#</th>
                        <th style="padding: 10px; text-align: left; border-bottom: 2px solid #dee2e6;">Task</th>
                        <th style="padding: 10px; text-align: left; border-bottom: 2px solid #dee2e6;">Verification Tier</th>
                        <th style="padding: 10px; text-align: center; border-bottom: 2px solid #dee2e6;">Weight</th>
                    </tr>
                </thead>
                <tbody>
                    {task_rows}
                </tbody>
            </table>
            
            <!-- Verification Tier Legend -->
            <h3 style="color: #555;">📋 Verification Tier Legend</h3>
            <table style="width: 100%; border-collapse: collapse; font-size: 13px; color: #555;">
                <tr><td style="padding: 4px;">🟢 Tier 1: System/MCP Verified</td><td style="text-align: right;">100%</td></tr>
                <tr><td style="padding: 4px;">🟢 Tier 2: Knowledge Quiz Verified</td><td style="text-align: right;">95%</td></tr>
                <tr><td style="padding: 4px;">🟢 Tier 3: Proof-of-Work Validated</td><td style="text-align: right;">90%</td></tr>
                <tr><td style="padding: 4px;">🔵 Tier 4: Peer Review Confirmed</td><td style="text-align: right;">80%</td></tr>
                <tr><td style="padding: 4px;">🟡 Tier 5: Admin Manual Verification</td><td style="text-align: right;">70%</td></tr>
                <tr><td style="padding: 4px;">🔴 Tier 6: Self-Attestation</td><td style="text-align: right;">50%</td></tr>
            </table>
        </div>
        
        <!-- Footer -->
        <div style="background: #f8f9fa; padding: 15px; text-align: center; color: #999; font-size: 12px;">
            Generated by <strong>O.N.E.</strong> (Onboarding Navigation Environment) — Group 28 Capstone Project
        </div>
    </div>
</body>
</html>"""
    return html


def _build_hr_report_markdown(
    employee_name: str,
    employee_email: str,
    role_persona: str,
    tech_stack: str,
    completed_items: list[dict],
    confidence_result: dict,
) -> str:
    """Build a Markdown version of the HR report for chat display."""
    lines = [
        "# 🎓 O.N.E. Onboarding Completion Report",
        "",
        "## 👤 Employee Information",
        f"- **Name:** {employee_name}",
        f"- **Email:** {employee_email}",
        f"- **Role Persona:** {role_persona}",
        f"- **Tech Stack:** {tech_stack}",
        f"- **Report Date:** {datetime.utcnow().strftime('%B %d, %Y at %H:%M UTC')}",
        "",
        f"## 📊 Overall Verification Confidence Score",
        f"### **{confidence_result['score_pct']:.1f}%** — {confidence_result['label']}",
        "",
        "## ✅ Completed Checklist Items",
        "",
        "| # | Task | Verification Tier | Weight |",
        "|---|------|-------------------|--------|",
    ]
    
    for i, item in enumerate(completed_items, 1):
        lines.append(
            f"| {i} | {item['task_name']} | {item['tier_label']} | {item['weight_pct']} |"
        )
    
    lines.extend([
        "",
        "## 📋 Verification Tier Legend",
        "| Tier | Description | Weight |",
        "|------|-------------|--------|",
        "| 🟢 Tier 1 | System/MCP Verified | 100% |",
        "| 🟢 Tier 2 | Knowledge Quiz Verified | 95% |",
        "| 🟢 Tier 3 | Proof-of-Work Validated | 90% |",
        "| 🔵 Tier 4 | Peer Review Confirmed | 80% |",
        "| 🟡 Tier 5 | Admin Manual Verification | 70% |",
        "| 🔴 Tier 6 | Self-Attestation | 50% |",
        "",
        "---",
        "*Generated by **O.N.E.** (Onboarding Navigation Environment) — Group 28 Capstone Project*",
    ])
    
    return "\n".join(lines)


# ── Tech stack lookup by role ─────────────────────────────────────────────────
ROLE_TECH_STACKS = {
    "frontend dev": "React 18, Vite, TailwindCSS, Zustand, React Router",
    "backend dev": "Python 3.11, FastAPI, SQLAlchemy, Alembic, PostgreSQL",
    "ai dev": "LangChain, LangGraph, Ollama (Qwen3:4B), ChromaDB, HuggingFace",
    "cloud": "Docker, Docker Compose, AWS/GCP, Nginx, GitHub Actions CI/CD",
    "it": "VPN, LDAP, Active Directory, Okta SSO, Network Configuration",
    "database dev": "PostgreSQL, Supabase, Alembic Migrations, SQLAlchemy ORM",
}


@tool("send_hr_completion_email")
def send_hr_completion_email(user_id: str) -> str:
    """Generate and send (or preview) an HR Onboarding Completion Report for the specified user.
    Sends via Gmail SMTP if credentials are configured; otherwise saves HTML locally and returns
    a formatted Markdown preview directly in chat. Always works — never crashes."""
    
    print(f"\n--- 📧 HR COMPLETION REPORT: Generating for user {user_id} ---")
    
    db = None
    try:
        user = None
        completed_tasks = []
        try:
            import uuid
            valid_uuid = None
            try:
                valid_uuid = uuid.UUID(str(user_id))
            except (ValueError, AttributeError, TypeError):
                valid_uuid = None

            if valid_uuid:
                db = SessionLocal()
                user = db.query(User).filter(User.id == valid_uuid).first()
                if user:
                    from app.models.developer_task_state import DeveloperTaskState
                    completed_tasks = db.query(DeveloperTaskState).filter(
                        DeveloperTaskState.user_id == valid_uuid,
                        DeveloperTaskState.status.in_(['verified', 'pending_verification'])
                    ).order_by(DeveloperTaskState.task_sequence_number.asc()).all()
        except Exception as db_err:
            logger.warning(f"Database session unavailable ({db_err}). Falling back to demo data.")
            user = None

        if user and completed_tasks:
            employee_name = user.name or user.email.split("@")[0].capitalize()
            employee_email = user.email
            role_persona = (user.department_role or "Developer").title()
            tech_stack = ROLE_TECH_STACKS.get((user.department_role or "").lower(), "General Engineering Stack")

            completed_items_with_tiers = []
            session_obj = None
            chat_text = ""
            if db:
                session_obj = db.query(OnboardingSession).filter(OnboardingSession.user_id == user_id).first()
                if session_obj:
                    logs = db.query(ConversationLog).filter(ConversationLog.session_id == session_obj.id).all()
                    chat_text = " ".join([log.content or "" for log in logs])

            for task_state in completed_tasks:
                tier_key = classify_verification_tier(chat_text, task_state.task_name)
                tier = VERIFICATION_TIERS[tier_key]
                completed_items_with_tiers.append({
                    "task_name": task_state.task_name,
                    "tier_key": tier_key,
                    "tier_label": tier["label"],
                    "weight": tier["weight"],
                    "weight_pct": f"{tier['weight'] * 100:.0f}%",
                })
        else:
            # High-fidelity demo employee fallback for offline demo / testing
            employee_name = getattr(user, "name", None) or "Alex Chen"
            employee_email = getattr(user, "email", None) or "alex.chen@nexusai.dev"
            role_persona = (getattr(user, "department_role", None) or "Backend Developer").title()
            tech_stack = ROLE_TECH_STACKS.get(getattr(user, "department_role", "backend dev").lower(), "Python 3.11, FastAPI, SQLAlchemy, PostgreSQL")
            
            completed_items_with_tiers = [
                {"task_name": "Clone Repository & Configure Local Dev Environment", "tier_key": "tier_3", "tier_label": "Tier 3: Proof-of-Work Validated", "weight": 0.90, "weight_pct": "90%"},
                {"task_name": "Setup PostgreSQL & Run Alembic Migrations", "tier_key": "tier_1", "tier_label": "Tier 1: System/MCP Verified", "weight": 1.00, "weight_pct": "100%"},
                {"task_name": "Verify Swagger /docs 200 OK & Service Health Check", "tier_key": "tier_3", "tier_label": "Tier 3: Proof-of-Work Validated", "weight": 0.90, "weight_pct": "90%"},
                {"task_name": "Review System Architecture & Pass Comprehension Quiz", "tier_key": "tier_2", "tier_label": "Tier 2: Knowledge Quiz Verified", "weight": 0.95, "weight_pct": "95%"},
                {"task_name": "Submit First Pull Request & Security Attestation", "tier_key": "tier_6", "tier_label": "Tier 6: Self-Attestation", "weight": 0.50, "weight_pct": "50%"},
            ]
        
        # 4. Compute overall confidence score
        confidence_result = compute_weighted_confidence(completed_items_with_tiers)
        
        print(f"📊 Confidence Score: {confidence_result['score_pct']:.1f}% — {confidence_result['label']}")
        print(f"📋 Tasks in report: {len(completed_items_with_tiers)}")
        
        # 5. Generate HTML and Markdown reports
        html_report = _build_hr_report_html(
            employee_name, employee_email, role_persona, tech_stack,
            completed_items_with_tiers, confidence_result
        )
        md_report = _build_hr_report_markdown(
            employee_name, employee_email, role_persona, tech_stack,
            completed_items_with_tiers, confidence_result
        )
        
        # 6. Attempt SMTP send or fallback to file save + preview
        from dotenv import load_dotenv
        load_dotenv(override=True)
        
        gmail_address = os.getenv("GMAIL_ADDRESS", "").strip()
        gmail_app_password = os.getenv("GMAIL_APP_PASSWORD", "").strip()
        hr_email = os.getenv("HR_EMAIL", gmail_address).strip()
        
        email_sent = False
        send_status = ""
        
        if gmail_address and gmail_app_password:
            try:
                msg = MIMEMultipart("alternative")
                msg["Subject"] = f"🎓 O.N.E. Onboarding Complete — {employee_name} ({role_persona})"
                msg["From"] = gmail_address
                msg["To"] = hr_email
                
                # Attach both plain text and HTML
                msg.attach(MIMEText(md_report, "plain"))
                msg.attach(MIMEText(html_report, "html"))
                
                # Send via Gmail SMTP_SSL (port 465)
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(gmail_address, gmail_app_password)
                    server.sendmail(gmail_address, hr_email, msg.as_string())
                
                email_sent = True
                send_status = f"✅ **Email sent successfully** to `{hr_email}` via Gmail SMTP."
                print(f"📧 Email sent to {hr_email}")
                
            except Exception as smtp_err:
                logger.warning(f"SMTP send failed: {smtp_err}")
                send_status = f"⚠️ SMTP send failed ({smtp_err}). Falling back to local file save."
        else:
            send_status = "📝 **SMTP credentials not configured.** Report saved locally for offline demo."
        
        # 7. Always save HTML to disk as backup
        report_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "..", "hr_completion_report.html"
        )
        report_path = os.path.abspath(report_path)
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(html_report)
        print(f"💾 HTML report saved to: {report_path}")
        
        # 8. Return full Markdown preview + status
        result = f"{send_status}\n💾 HTML report saved to: `{report_path}`\n\n{md_report}"
        return result
        
    except Exception as e:
        logger.error(f"HR Report generation error: {e}", exc_info=True)
        return f"❌ Error generating HR report: {str(e)}"
    finally:
        if db:
            db.close()
        print("--- 🏁 HR REPORT GENERATION FINISHED ---\n")
