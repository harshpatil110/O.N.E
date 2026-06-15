import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv(override=True)

from app.core.database import SessionLocal
from app.models.user import User
from app.models.onboarding_session import OnboardingSession
from app.models.conversation_log import ConversationLog

def seed_dashboard_data():
    db = SessionLocal()
    try:
        progress_map = {
            "parth@gmail.com": 40,
            "manas@gmail.com": 60,
            "archit@gmail.com": 76
        }

        users = db.query(User).filter(User.email.in_(progress_map.keys())).all()
        if not users:
            print("No users found to seed.")
            return
            
        for user in users:
            # Check for existing session or create one
            session = db.query(OnboardingSession).filter(OnboardingSession.user_id == user.id).first()
            if not session:
                session = OnboardingSession(
                    user_id=user.id,
                    status="in_progress",
                    started_at=datetime.utcnow() - timedelta(days=7),
                    progress_percentage=0
                )
                db.add(session)
                db.commit()
                db.refresh(session)
            
            # Update progress
            session.progress_percentage = progress_map[user.email]
            
            # To prevent duplicating logs infinitely if run multiple times, 
            # we don't strictly *delete* old logs, but maybe we could. 
            # We'll just append.
            
            print(f"Seeding chat logs for {user.email}...")
            # We want around 5-10 messages per day over the last 7 days
            for day_offset in range(7):
                # Ensure the time varies
                date_for_log = datetime.utcnow() - timedelta(days=day_offset)
                
                num_logs = random.randint(2, 10)
                for i in range(num_logs):
                    log = ConversationLog(
                        session_id=session.id,
                        role=random.choice(["user", "assistant"]),
                        content=f"Dummy log {i} for {user.email} on day -{day_offset}",
                        created_at=date_for_log - timedelta(hours=random.randint(1, 10))
                    )
                    db.add(log)
            
        db.commit()
        print("Dashboard data successfully seeded!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_dashboard_data()
