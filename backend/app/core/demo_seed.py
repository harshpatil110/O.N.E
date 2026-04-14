import uuid
import logging
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.onboarding_session import OnboardingSession
from app.models.checklist_item import ChecklistItem
from app.models.conversation_log import ConversationLog
from app.core.security import hash_password

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_demo_data():
    db: Session = SessionLocal()
    try:
        logger.info("Clearing existing data...")
        # Clear data in reverse order of dependencies
        db.query(ConversationLog).delete()
        db.query(ChecklistItem).delete()
        db.query(OnboardingSession).delete()
        db.query(User).delete()
        db.commit()

        logger.info("Creating HR Admin...")
        admin_pw = hash_password("123456")
        hr_admin = User(
            name="HR Admin",
            email="patilha2005@gmail.com",
            hashed_password=admin_pw,
            role="hr_admin"
        )
        db.add(hr_admin)

        logger.info("Creating Employees...")
        # Password for all demo users
        demo_pw = hash_password("123456")

        # 1. Harsh (Live demo user - no session)
        harsh = User(
            name="Harsh Patil",
            email="harsh@gmail.com",
            hashed_password=demo_pw,
            role="employee"
        )
        db.add(harsh)

        # 2. Parth (20% complete)
        parth = User(
            name="Parth Shah",
            email="parth@gmail.com",
            hashed_password=demo_pw,
            role="employee"
        )
        db.add(parth)
        db.flush() # Get parth.id

        # 3. Manas (66% complete)
        manas = User(
            name="Manas Gupta",
            email="manas@gmail.com",
            hashed_password=demo_pw,
            role="employee"
        )
        db.add(manas)
        db.flush()

        # 4. Archit (75% complete)
        archit = User(
            name="Archit Verma",
            email="archit@gmail.com",
            hashed_password=demo_pw,
            role="employee"
        )
        db.add(archit)
        db.flush()

        # Create Sessions
        now = datetime.now(timezone.utc)
        
        # Parth's Session (Started 2 days ago)
        parth_session = OnboardingSession(
            user_id=parth.id,
            status="in_progress",
            current_fsm_state="ONBOARDING_EXECUTION",
            started_at=now - timedelta(days=2),
            persona={"role": "backend", "experience_level": "mid", "tech_stack": ["Python", "FastAPI"]}
        )
        db.add(parth_session)
        db.flush()

        # Manas's Session (Started 1 day ago)
        manas_session = OnboardingSession(
            user_id=manas.id,
            status="in_progress",
            current_fsm_state="ONBOARDING_EXECUTION",
            started_at=now - timedelta(days=1),
            persona={"role": "frontend", "experience_level": "junior", "tech_stack": ["React", "Tailwind"]}
        )
        db.add(manas_session)
        db.flush()

        # Archit's Session (Started 3 days ago)
        archit_session = OnboardingSession(
            user_id=archit.id,
            status="in_progress",
            current_fsm_state="ONBOARDING_EXECUTION",
            started_at=now - timedelta(days=3),
            persona={"role": "devops", "experience_level": "senior", "tech_stack": ["Docker", "Kubernetes"]}
        )
        db.add(archit_session)
        db.flush()

        # Helper to create checklist items
        def add_items(session_id, count, completed_count):
            categories = ["General", "Access", "Security", "Development"]
            for i in range(count):
                status = "completed" if i < completed_count else "pending"
                item = ChecklistItem(
                    session_id=session_id,
                    item_key=f"item_{i}",
                    title=f"Onboarding Task {i+1}",
                    description=f"Description for task {i+1}",
                    category=categories[i % len(categories)],
                    sort_order=i,
                    status=status,
                    completed_at=now - timedelta(hours=2) if status == "completed" else None
                )
                db.add(item)

        # Parth: 10 items, 2 completed (20%)
        add_items(parth_session.id, 10, 2)

        # Manas: 12 items, 8 completed (66.6%)
        add_items(manas_session.id, 12, 8)

        # Archit: 12 items, 9 completed (75%)
        add_items(archit_session.id, 12, 9)

        db.commit()
        logger.info("Successfully seeded demo data!")
        
        print("\n" + "="*50)
        print("🚀 O.N.E. Demo Seeding Complete")
        print("="*50)
        print(f"Admin Access:")
        print(f"  Email: patilha2005@gmail.com")
        print(f"  Password: 123456")
        print("\nEmployee Access (All use password: 123456):")
        print(f"  - harsh@gmail.com (Live Demo - 0%)")
        print(f"  - parth@gmail.com (Progress: 20%)")
        print(f"  - manas@gmail.com (Progress: 66%)")
        print(f"  - archit@gmail.com (Progress: 75%)")
        print("="*50 + "\n")

    except Exception as e:
        db.rollback()
        logger.error(f"Seeding failed: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_demo_data()
