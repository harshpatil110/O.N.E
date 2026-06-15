"""
seed_admin_dashboard.py
───────────────────────
Ultimate seeder for the O.N.E. Admin Dashboard.
Handles schema forcing, progress injection, and analytics data generation.
"""

import os
import random
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# ── CRITICAL: override any cached env values ──
load_dotenv(override=True)

from sqlalchemy import text
from app.core.database import engine, SessionLocal, Base
from app.models.user import User
from app.models.onboarding_session import OnboardingSession
from app.models.conversation_log import ConversationLog

# ──────────────────────────────────────────────────────────
# Step 0: Force schema sync (bypass Alembic if needed)
# ──────────────────────────────────────────────────────────
def force_schema_sync():
    """Ensure all model columns exist in Supabase, creating any missing ones."""
    print("[1/4] Forcing schema sync with Base.metadata.create_all()...")
    Base.metadata.create_all(bind=engine)
    
    # Also explicitly ensure progress_percentage column exists
    with engine.connect() as conn:
        try:
            conn.execute(text(
                "ALTER TABLE onboarding_sessions "
                "ADD COLUMN IF NOT EXISTS progress_percentage INTEGER DEFAULT 0 NOT NULL"
            ))
            conn.commit()
            print("  [OK] progress_percentage column verified in onboarding_sessions")
        except Exception as e:
            print(f"  [i] Column check note: {e}")

# ──────────────────────────────────────────────────────────
# Step 1: Inject progress percentages
# ──────────────────────────────────────────────────────────
PROGRESS_MAP = {
    "parth@gmail.com": 40,
    "manas@gmail.com": 60,
    "archit@gmail.com": 76,
}

def inject_progress(db):
    print("[2/4] Injecting progress percentages...")
    users = db.query(User).filter(User.email.in_(PROGRESS_MAP.keys())).all()
    
    if not users:
        print("  [FAIL] No matching users found. Aborting progress injection.")
        return {}

    user_session_map = {}  # email -> session_id (for log seeding)
    
    for user in users:
        target_pct = PROGRESS_MAP[user.email]
        
        # Ensure an OnboardingSession exists
        session = db.query(OnboardingSession).filter(
            OnboardingSession.user_id == user.id
        ).first()
        
        if not session:
            session = OnboardingSession(
                user_id=user.id,
                status="in_progress",
                started_at=datetime.now(timezone.utc) - timedelta(days=random.randint(5, 10)),
                progress_percentage=target_pct,
            )
            db.add(session)
            db.flush()
            print(f"  + Created session for {user.email}")
        else:
            session.progress_percentage = target_pct
        
        user_session_map[user.email] = session.id
        print(f"  [OK] {user.email} -> {target_pct}%")
    
    db.commit()
    return user_session_map

# ──────────────────────────────────────────────────────────
# Step 2: Generate realistic ConversationLog entries
# ──────────────────────────────────────────────────────────

# Controlled per-day volume so the chart looks dynamic
DAY_VOLUME = {
    0: 10,   # Monday
    1: 45,   # Tuesday   ← spike
    2: 15,   # Wednesday
    3: 32,   # Thursday
    4: 28,   # Friday
    5: 8,    # Saturday
    6: 5,    # Sunday
}

SAMPLE_QUESTIONS = [
    "How do I set up the company VPN?",
    "Where can I find AWS access keys?",
    "Who do I contact for GitHub access?",
    "What's the deployment pipeline process?",
    "How does the CI/CD system work here?",
    "Where is the internal documentation wiki?",
    "How do I request a staging environment?",
    "What are the code review guidelines?",
    "How do I set up my local development environment?",
    "Who approves production deployments?",
]

SAMPLE_ANSWERS = [
    "You can configure the VPN by following the guide in Confluence under 'IT Setup'.",
    "AWS access keys are managed through the IT portal. Submit a request ticket.",
    "For GitHub access, reach out to your team lead or the DevOps channel on Slack.",
    "Our deployment pipeline uses GitHub Actions. Check the .github/workflows directory.",
    "The CI/CD system runs on GitHub Actions with automated testing and staging deploys.",
    "The internal wiki is hosted at wiki.company.internal. Ask IT for your login.",
    "Staging environments can be requested through the DevOps self-service portal.",
    "Code reviews require at least 2 approvals. See the CONTRIBUTING.md in each repo.",
    "Follow the README.md in the project root. It has step-by-step local setup instructions.",
    "Production deployments require sign-off from the Engineering Manager and QA lead.",
]


def seed_conversation_logs(db, user_session_map):
    print("[3/4] Generating 7-day conversation log history...")
    
    # Clean existing dummy logs to prevent duplicates on re-runs
    for email, session_id in user_session_map.items():
        existing = db.query(ConversationLog).filter(
            ConversationLog.session_id == session_id,
            ConversationLog.content.like("Dummy log%")  # only delete old dummy data
        ).all()
        for log in existing:
            db.delete(log)
    db.commit()
    print("  [i] Cleared previous dummy logs")
    
    total_created = 0
    
    for email, session_id in user_session_map.items():
        for day_offset in range(7):
            target_date = datetime.now(timezone.utc) - timedelta(days=day_offset)
            weekday = target_date.weekday()
            
            # Split the target volume across users (roughly equal)
            per_user_volume = max(DAY_VOLUME[weekday] // len(user_session_map), 1)
            
            for i in range(per_user_volume):
                # Alternate user/assistant messages
                hour_offset = random.randint(8, 20)  # business-ish hours
                minute_offset = random.randint(0, 59)
                log_time = target_date.replace(
                    hour=hour_offset, minute=minute_offset, second=random.randint(0, 59)
                )
                
                q_idx = random.randint(0, len(SAMPLE_QUESTIONS) - 1)
                
                # User question
                db.add(ConversationLog(
                    session_id=session_id,
                    role="user",
                    content=SAMPLE_QUESTIONS[q_idx],
                    created_at=log_time,
                ))
                
                # Assistant answer (a few seconds later)
                db.add(ConversationLog(
                    session_id=session_id,
                    role="assistant",
                    content=SAMPLE_ANSWERS[q_idx],
                    created_at=log_time + timedelta(seconds=random.randint(2, 30)),
                ))
                
                total_created += 2
        
        print(f"  [OK] Seeded logs for {email}")
    
    db.commit()
    print(f"  [OK] Total conversation log entries created: {total_created}")


# ──────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  O.N.E. Admin Dashboard — Ultimate Seeder")
    print("=" * 60)
    
    force_schema_sync()
    
    db = SessionLocal()
    try:
        user_session_map = inject_progress(db)
        
        if user_session_map:
            seed_conversation_logs(db, user_session_map)
        
        print("[4/4] Verification...")
        # Quick verification query
        sessions = db.query(OnboardingSession, User).join(
            User, OnboardingSession.user_id == User.id
        ).filter(User.email.in_(PROGRESS_MAP.keys())).all()
        
        for session, user in sessions:
            log_count = db.query(ConversationLog).filter(
                ConversationLog.session_id == session.id
            ).count()
            print(f"  [OK] {user.email}: progress={session.progress_percentage}%, logs={log_count}")
        
        print("\n[DONE] Seeding complete!")
        
    except Exception as e:
        db.rollback()
        print(f"\n[FAIL] Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
