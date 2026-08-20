from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, String
from app.core.database import get_db
from app.models.user import User
from app.models.conversation_log import ConversationLog
from app.models.onboarding_session import OnboardingSession
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from datetime import datetime, timedelta

router = APIRouter(prefix="/admin", tags=["Admin Analytics"])

# Initialize the local LLM for analytics processing
analytics_llm = ChatOllama(model="qwen2.5:3b", temperature=0.2)

@router.get("/dashboard-stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    try:
        total_devs = db.query(User).count()
        
        # Calculate Average Progress
        avg_progress = db.query(func.avg(User.onboarding_progress)).scalar() or 0.0
        
        # Calculate how many devs are stuck (e.g., progress == 0)
        stuck_devs = db.query(User).filter(User.onboarding_progress == 0).count()
        
        return {
            "total_developers": total_devs,
            "average_completion_rate": round(avg_progress, 1),
            "stuck_developers": stuck_devs,
            "avg_time_to_onboard_days": 0 # Placeholder for Phase 4 logic
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/developers")
def get_all_developers(db: Session = Depends(get_db)):
    devs = db.query(User).all()
    return [
        {
            "id": str(d.id),
            "name": d.email.split('@')[0].capitalize() if d.email else "Unknown",
            "email": d.email,
            "progress": d.onboarding_progress or 0,
            "role": d.department_role
        } 
        for d in devs
    ]

@router.get("/analytics/topics")
def get_topic_distribution(db: Session = Depends(get_db)):
    try:
        # Fetch all human queries
        logs = db.query(ConversationLog).filter(ConversationLog.role == 'user').all()
        
        categories = {
            "knowledge_base": 0,
            "task_list": 0,
            "github": 0,
            "conversation_history": 0,
            "other": 0
        }
        
        total_queries = len(logs)
        if total_queries == 0:
            return {"distribution": categories, "total": 0}

        # Simple Categorization Engine
        for log in logs:
            msg = log.content.lower() if log.content else ""
            if any(kw in msg for kw in ["policy", "document", "how to", "setup", "guide", "manual"]):
                categories["knowledge_base"] += 1
            elif any(kw in msg for kw in ["task", "todo", "done", "complete", "next step", "checklist"]):
                categories["task_list"] += 1
            elif any(kw in msg for kw in ["github", "repo", "pull request", "pr", "commit", "branch"]):
                categories["github"] += 1
            elif any(kw in msg for kw in ["history", "previous", "earlier", "context", "my name"]):
                categories["conversation_history"] += 1
            else:
                categories["other"] += 1
                
        # Calculate percentages
        distribution = {k: round((v / total_queries) * 100, 1) for k, v in categories.items()}
        
        return {
            "total_queries": total_queries,
            "raw_counts": categories,
            "percentages": distribution
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/insights")
def get_ai_insights(db: Session = Depends(get_db)):
    try:
        # 1. Gather live metrics
        total_devs = db.query(User).count()
        avg_progress = db.query(func.avg(User.onboarding_progress)).scalar() or 0.0
        stuck_devs = db.query(User).filter(User.onboarding_progress == 0).count()
        
        logs = db.query(ConversationLog).filter(ConversationLog.role == 'user').all()
        topics = {"knowledge_base": 0, "task_list": 0, "github": 0, "other": 0}
        for log in logs:
            msg = log.content.lower() if log.content else ""
            if any(kw in msg for kw in ["policy", "document", "how to"]): topics["knowledge_base"] += 1
            elif any(kw in msg for kw in ["task", "todo", "done"]): topics["task_list"] += 1
            elif any(kw in msg for kw in ["github", "repo", "pr"]): topics["github"] += 1
            else: topics["other"] += 1

        top_topic = max(topics, key=topics.get).replace("_", " ").title() if logs else "None"

        # 2. Determine Intervention Level securely in Python
        if stuck_devs > 0 or avg_progress < 20:
            level = "CRITICAL"
            title = "Intervention Required"
        elif stuck_devs == 0 and avg_progress >= 80:
            level = "NOMINAL"
            title = "System Healthy"
        else:
            level = "WARNING"
            title = "Monitor Progress"

        # 3. Prompt the LLM for a qualitative insight
        sys_prompt = "You are O.N.E., an AI administrative assistant analyzing developer onboarding metrics. Be extremely concise. Generate a 2-sentence insight summarizing the current team status and suggesting one action based on the data."
        human_prompt = f"Data: {total_devs} total devs, {stuck_devs} stuck at 0%. Average progress: {round(avg_progress, 1)}%. Most asked topic: {top_topic}. Write the insight."

        response = analytics_llm.invoke([
            SystemMessage(content=sys_prompt),
            HumanMessage(content=human_prompt)
        ])
        
        insight_text = response.content if hasattr(response, 'content') else str(response)

        return {
            "advisory_level": level,
            "advisory_title": title,
            "stuck_count": stuck_devs,
            "ai_insight": insight_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/developers/{user_id}/chats")
def get_developer_chats(user_id: str, db: Session = Depends(get_db)):
    print(f"\n--- 🔍 ADMIN CHAT FETCH INITIATED ---")
    print(f"Target User ID: {user_id}")
    try:
        session = db.query(OnboardingSession).filter(OnboardingSession.user_id == user_id).first()
        if not session:
            print(f"❌ No OnboardingSession found for user: {user_id}")
            return {"status": "success", "logs": []}
            
        # Cast session_id to string to prevent UUID mapping errors in SQLAlchemy
        logs = db.query(ConversationLog).filter(
            cast(ConversationLog.session_id, String) == str(session.id)
        ).order_by(ConversationLog.created_at.asc()).all()
        
        print(f"✅ Found {len(logs)} logs for this user (session {session.id}).")
        
        # Strictly format the output
        formatted_logs = [
            {
                "role": log.role,
                "message": log.content,
                "timestamp": log.created_at.isoformat() if log.created_at else None
            }
            for log in logs
        ]
        
        print(f"--- 📤 RETURNING DATA TO FRONTEND ---\n")
        return {"status": "success", "logs": formatted_logs}
        
    except Exception as e:
        print(f"❌ DATABASE FETCH ERROR: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/advanced")
def get_advanced_analytics(db: Session = Depends(get_db)):
    try:
        users = db.query(User).all()
        
        frustration_index = []
        autonomy_radar = []
        proficiency_matrix = []
        task_velocity = []

        for user in users:
            session = db.query(OnboardingSession).filter(OnboardingSession.user_id == user.id).first()
            if not session:
                continue
                
            logs = db.query(ConversationLog).filter(
                ConversationLog.session_id == session.id,
                ConversationLog.role == 'user'
            ).order_by(ConversationLog.created_at.asc()).all()
            
            total_msgs = len(logs)
            name = user.name or f"Dev {user.id}"
            progress = user.onboarding_progress or 0
            
            # Use email split if available
            display_name = user.email.split('@')[0] if hasattr(user, 'email') and user.email else name

            # 1. Frustration Index
            if total_msgs == 0:
                frustration_score = 0
            else:
                neg_count = sum(1 for log in logs if log.content and any(kw in log.content.lower() for kw in ["error", "stuck", "fail", "bug", "help", "broken", "issue"]))
                frustration_score = round((neg_count / total_msgs) * 100, 1)
                
            frustration_index.append({"name": display_name, "score": frustration_score})
            
            # 2. Autonomy vs AI Reliance
            reliance = min(10, (total_msgs / 10.0))
            autonomy = (progress / 10.0) - reliance
            autonomy = max(0, min(10, autonomy + 5))
            autonomy_radar.append({
                "subject": display_name,
                "autonomy": round(autonomy, 1),
                "reliance": round(reliance, 1)
            })

            # 3. Proficiency Matrix
            tech_kws = ["architecture", "database", "api", "auth", "deploy", "docker", "optimization"]
            tech_depth = sum(10 for log in logs if log.content and any(kw in log.content.lower() for kw in tech_kws))
            base_depth = 20 + tech_depth
            proficiency_matrix.append({
                "name": display_name, 
                "progress": progress, 
                "depth": min(100, base_depth)
            })
            
            # 4. Task Velocity
            all_logs = db.query(ConversationLog).filter(
                ConversationLog.session_id == session.id
            ).order_by(ConversationLog.created_at.asc()).all()
            
            if len(all_logs) < 2:
                task_velocity.append({"name": display_name, "hours": 0})
            else:
                first_interaction = all_logs[0].created_at
                last_interaction = all_logs[-1].created_at
                time_diff = last_interaction - first_interaction
                hours = round(time_diff.total_seconds() / 3600, 2)
                
                if hours == 0 and time_diff.total_seconds() > 0:
                    hours = 0.01 
                    
                task_velocity.append({"name": display_name, "hours": hours})

        return {
            "frustration_index": frustration_index,
            "autonomy_radar": autonomy_radar,
            "proficiency_matrix": proficiency_matrix,
            "task_velocity": task_velocity
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/seed-analytics-data")
def seed_dummy_analytics_data(db: Session = Depends(get_db)):
    try:
        users = db.query(User).all()
        if not users:
            return {"message": "No users found to seed."}

        logs_to_add = []
        base_time = datetime.utcnow() - timedelta(days=2) # Start 2 days ago

        for i, user in enumerate(users):
            session = db.query(OnboardingSession).filter(OnboardingSession.user_id == user.id).first()
            if not session:
                continue
                
            # 1. First Interaction
            logs_to_add.append(ConversationLog(
                session_id=session.id, role='user', 
                content="What is my first task?", 
                created_at=base_time
            ))
            
            # 2. Time-gapped Interaction (Fixes Task Velocity)
            # Give different users different hour gaps (e.g., User 0 takes 1 hour, User 1 takes 4 hours)
            gap_hours = (i + 1) * 1.5 
            second_time = base_time + timedelta(hours=gap_hours)
            
            # 3. Keyword Injection (Fixes Frustration Index)
            # Alternate injecting frustration keywords
            if i % 2 == 0:
                msg = "I am completely stuck on this error. It is failing to build."
            else:
                msg = "I finished the setup. What is next?"
                
            logs_to_add.append(ConversationLog(
                session_id=session.id, role='user', 
                content=msg, 
                created_at=second_time
            ))

        db.add_all(logs_to_add)
        db.commit()
        return {"message": f"Successfully seeded {len(logs_to_add)} logs to populate charts."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
