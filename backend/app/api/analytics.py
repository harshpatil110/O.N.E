import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.core.auth_deps import get_hr_admin_user
from app.models.onboarding_session import OnboardingSession
from app.models.user import User
from app.models.checklist_item import ChecklistItem
from app.models.conversation_log import ConversationLog
from app.schemas.analytics import (
    DeepDiveAnalyticsResponse, QuantitativeData, QualitativeData, 
    CompletionMatrixItem, TaskVelocityItem, DeveloperInsight, 
    TopicDistributionItem, LaggingDeveloper
)
from app.services.analytics_service import AnalyticsService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/hr/analytics", tags=["analytics"], dependencies=[Depends(get_hr_admin_user)])

@router.get("/deep-dive", response_model=DeepDiveAnalyticsResponse)
async def get_deep_dive_analytics(db: Session = Depends(get_db)):
    # Calculate Quantitative Data
    sessions_query = db.query(OnboardingSession, User).join(User, OnboardingSession.user_id == User.id).filter(OnboardingSession.status == "in_progress").all()
    
    completion_matrix = []
    sessions_data = []
    chat_histories = {}
    total_percent = 0
    
    for session_record, user_record in sessions_query:
        dev_id = str(session_record.id)
        name = user_record.name or "Unknown"

        # Calculate Completion Percentage
        checklist_stats = db.query(
            func.count(ChecklistItem.id).label("total"),
            func.count(ChecklistItem.id).filter(ChecklistItem.status == "completed").label("completed")
        ).filter(ChecklistItem.session_id == session_record.id).first()
        
        total_items = checklist_stats.total if checklist_stats and checklist_stats.total else 0
        completed_items = checklist_stats.completed if checklist_stats and checklist_stats.completed else 0
        percent_complete = round((completed_items / total_items) * 100) if total_items > 0 else 0
        
        total_percent += percent_complete
        
        completion_matrix.append(
            CompletionMatrixItem(
                developer_id=dev_id,
                employee_name=name,
                percent_complete=percent_complete
            )
        )
        
        sessions_data.append({
            "id": dev_id,
            "name": name,
            "percent_complete": percent_complete
        })
        
        # Build chat history for this user
        chat_logs = db.query(ConversationLog).filter(
            ConversationLog.session_id == session_record.id,
            ConversationLog.role.in_(['user', 'assistant'])
        ).order_by(ConversationLog.created_at.asc()).all()
        
        chat_histories[dev_id] = [
            {"role": log.role, "content": log.content} for log in chat_logs
        ]

    # Overall Completion
    overall_completion = float(total_percent) / len(sessions_query) if sessions_query else 0.0

    # Task Velocity
    completed_items_query = db.query(ChecklistItem, OnboardingSession.started_at)\
        .join(OnboardingSession, ChecklistItem.session_id == OnboardingSession.id)\
        .filter(ChecklistItem.status == "completed", ChecklistItem.completed_at != None).all()
        
    task_groups = {}
    for item, started_at in completed_items_query:
        if not started_at or not item.completed_at:
            continue
            
        duration_hours = (item.completed_at - started_at).total_seconds() / 3600.0
        if duration_hours < 0: duration_hours = 0.5
        
        key = item.item_key or item.title
        if key not in task_groups:
            task_groups[key] = {"title": item.title, "durations": []}
        task_groups[key]["durations"].append(duration_hours)

    task_velocity = []
    for key, group in task_groups.items():
        avg_hours = sum(group["durations"]) / len(group["durations"])
        task_velocity.append(
            TaskVelocityItem(
                task_id=key,
                title=group["title"],
                avg_duration_hours=round(avg_hours, 2)
            )
        )

    quantitative_data = QuantitativeData(
        overall_completion=round(overall_completion, 2),
        completion_matrix=completion_matrix,
        task_velocity=task_velocity
    )

    # Calculate Qualitative AI insights
    insights_engine = AnalyticsService()
    try:
        ai_result = await insights_engine.generate_ai_insights(sessions_data, chat_histories)
    except Exception as e:
        logger.error(f"AI Insights failed: {e}")
        ai_result = {"developer_insights": [], "topic_distribution": [], "lagging_developer": None}
    
    # Safely Map Dict results into Pydantic models
    developer_insights = []
    for insight in ai_result.get("developer_insights", []):
         developer_insights.append(DeveloperInsight(
             developer_id=str(insight.get("developer_id", "")),
             employee_name=str(insight.get("employee_name", "Unknown")),
             question_complexity_score=int(insight.get("question_complexity_score", 5)),
             question_severity=str(insight.get("question_severity", "Medium"))
         ))
         
    topic_distribution = []
    for td in ai_result.get("topic_distribution", []):
        topic_distribution.append(TopicDistributionItem(
             topic=str(td.get("topic", "Unknown")),
             percentage=float(td.get("percentage", 0.0))
        ))
        
    lag_dev_data = ai_result.get("lagging_developer")
    lagging_developer = None
    if lag_dev_data and isinstance(lag_dev_data, dict) and lag_dev_data.get("developer_id"):
         lagging_developer = LaggingDeveloper(
             developer_id=str(lag_dev_data.get("developer_id", "")),
             risk_summary=str(lag_dev_data.get("risk_summary", ""))
         )
         
    qualitative_data = QualitativeData(
         developer_insights=developer_insights,
         topic_distribution=topic_distribution,
         lagging_developer=lagging_developer
    )
    
    return DeepDiveAnalyticsResponse(
        quantitative=quantitative_data,
        qualitative=qualitative_data
    )
