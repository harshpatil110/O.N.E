import logging
from typing import Optional, List
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func, select, and_

logger = logging.getLogger(__name__)

from app.core.database import get_db
from app.core.auth_deps import get_hr_admin_user
from app.models.user import User
from app.models.onboarding_session import OnboardingSession
from app.models.checklist_item import ChecklistItem
from app.schemas.admin import PaginatedSessions, SessionSummary, AdminMetrics
from app.services.hr_notification_service import HRNotificationService

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(get_hr_admin_user)])

@router.get("/sessions", response_model=PaginatedSessions)
async def list_sessions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    role: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    List all onboarding sessions with pagination and filters.
    Includes employee details and completion percentage.
    """
    query = db.query(OnboardingSession, User).join(User, OnboardingSession.user_id == User.id)
    
    if role:
        query = query.filter(User.role == role)
    if status:
        query = query.filter(OnboardingSession.status == status)
        
    total = query.count()
    
    # Apply pagination
    results = query.offset((page - 1) * page_size).limit(page_size).all()
    
    items = []
    for session_record, user_record in results:
        # Calculate completion percentage
        # We query for this session's checklist items
        checklist_stats = db.query(
            func.count(ChecklistItem.id).label("total"),
            func.count(ChecklistItem.id).filter(ChecklistItem.status == "completed").label("completed")
        ).filter(ChecklistItem.session_id == session_record.id).first()
        
        total_items = checklist_stats.total if checklist_stats else 0
        completed_items = checklist_stats.completed if checklist_stats else 0
        percent_complete = round((completed_items / total_items) * 100) if total_items > 0 else 0
        
        items.append(SessionSummary(
            session_id=str(session_record.id),
            employee_name=user_record.name or "Unknown",
            employee_email=user_record.email or "",
            role=user_record.role or "employee",
            status=session_record.status,
            started_at=session_record.started_at,
            completed_at=session_record.completed_at,
            percent_complete=percent_complete
        ))
        
    return PaginatedSessions(
        items=items,
        total=total,
        page=page,
        page_size=page_size
    )

@router.get("/metrics", response_model=AdminMetrics)
async def get_metrics(db: Session = Depends(get_db)):
    """
    Calculate high-level metrics for the HR dashboard.
    """
    # Total sessions
    total_sessions = db.query(OnboardingSession).count()
    
    # Active vs Completed
    active_sessions = db.query(OnboardingSession).filter(OnboardingSession.status == "in_progress").count()
    completed_sessions = db.query(OnboardingSession).filter(OnboardingSession.status == "completed").count()
    
    # Completion Rate
    completion_rate = (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0.0
    
    # Avg Duration in Hours for completed sessions
    # Note: Using SQLAlchemy's func.avg and handling the interval if possible, 
    # but simplest is to fetch and calculate or use a raw SQL approach if dialect allows.
    # For PostgreSQL: AVG(completed_at - started_at)
    avg_duration_query = db.query(
        func.avg(OnboardingSession.completed_at - OnboardingSession.started_at)
    ).filter(OnboardingSession.status == "completed").scalar()
    
    avg_duration_hours = 0.0
    if avg_duration_query:
        # avg_duration_query is typically a timedelta object in SQLAlchemy/Postgres
        try:
            if hasattr(avg_duration_query, "total_seconds"):
                avg_duration_hours = avg_duration_query.total_seconds() / 3600.0
            else:
                # Fallback for unexpected types
                logger.warning(f"Unexpected type for avg_duration_query: {type(avg_duration_query)}")
        except Exception as e:
            logger.error(f"Error calculating average duration: {str(e)}")
        
    # Completions this week (last 7 days)
    seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
    completions_this_week = db.query(OnboardingSession).filter(
        OnboardingSession.status == "completed",
        OnboardingSession.completed_at >= seven_days_ago
    ).count()
    
    return AdminMetrics(
        total_sessions=total_sessions,
        active_sessions=active_sessions,
        completed_sessions=completed_sessions,
        completion_rate=completion_rate,
        avg_duration_hours=avg_duration_hours,
        completions_this_week=completions_this_week
    )

@router.post("/notify-hr/{session_id}")
async def resend_hr_notification(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Manually trigger the HR notification email for a specific session.
    """
    hr_service = HRNotificationService(db)
    success = await hr_service.send_completion_email(session_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send notification email. Please check server logs."
        )
        
    return {"success": True}
