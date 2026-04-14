import logging
from datetime import datetime
from sqlalchemy.orm import Session
from app.services.email_service import EmailService
from app.services.email_template import generate_completion_email_html
from app.models.onboarding_session import OnboardingSession
from app.models.user import User
from app.models.checklist_item import ChecklistItem

logger = logging.getLogger(__name__)

class HRNotificationService:
    """
    Service responsible for finalizing onboarding sessions and notifying HR.
    """
    def __init__(self, db: Session):
        """
        Initialize the service with a DB session.
        """
        self.db = db
        self.email_service = EmailService()

    def calculate_confidence(self, checklist: list) -> int:
        """
        Calculate a confidence score based on the completion of required items.

        Args:
            checklist (list): List of ChecklistItem objects.

        Returns:
            int: Percentage score (0-100).
        """
        required = [i for i in checklist if i.required]
        completed_required = [i for i in required if i.status == "completed"]
        if not required:
            return 100
        return round(len(completed_required) / len(required) * 100)

    async def send_completion_email(self, session_id: str) -> bool:
        """
        Gathers session metrics, generates a completion report, and sends it to HR.

        Args:
            session_id (str): The unique ID of the onboarding session.

        Returns:
            bool: True if the notification was sent and database updated.
        """
        # 1. Load session and user from DB
        session = self.db.query(OnboardingSession).filter_by(id=session_id).first()
        if not session:
            logger.error(f"Session {session_id} not found.")
            return False
            
        user = self.db.query(User).filter_by(id=session.user_id).first()
        if not user:
            logger.error(f"User not found for session {session_id}.")
            return False

        # 2. Load all checklist items for this session
        checklist = self.db.query(ChecklistItem).filter_by(session_id=session_id).all()

        # 3. Calculate confidence score
        confidence_score = self.calculate_confidence(checklist)

        # 4. Calculate duration
        completed_at = session.completed_at or datetime.utcnow()
        duration_delta = completed_at - session.started_at
        duration_hours = duration_delta.total_seconds() / 3600.0

        # 5. Generate HTML email
        html_body = generate_completion_email_html(
            user=user,
            session=session,
            checklist=checklist,
            confidence_score=confidence_score,
            duration_hours=duration_hours
        )

        # 6. Send to HR email, CC developer email
        subject = f"Onboarding Completed - {user.name} ({user.role})"
        success = await self.email_service.send_email(
            to=self.email_service.hr_email,
            subject=subject,
            html_body=html_body,
            cc=[user.email]
        )

        # 7. Update session if successful
        if success:
            session.hr_notified = True
            session.completed_at = completed_at
            session.status = "completed"
            self.db.commit()
            logger.info(f"Successfully finalized session {session_id} and notified HR.")
            return True
            
        return False
