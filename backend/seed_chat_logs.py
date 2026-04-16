import sys
import os
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

# Add the root directory to sys.path so 'app' is importable
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.user import User
from app.models.onboarding_session import OnboardingSession
from app.models.conversation_log import ConversationLog

def seed_chat_logs():
    db = SessionLocal()
    print("Connecting to the database...")

    targets = {
        "parth@gmail.com": [
            {"role": "assistant", "content": "Welcome to O.N.E! I am your Onboarding Agent. Can you confirm your primary role here so I can tailor your task list?"},
            {"role": "user", "content": "I am a Data Engineer."},
            {"role": "assistant", "content": "Excellent! I have configured your environment for data engineering. Your first task is to set up your local Postgres database. Let me know when you start."},
            {"role": "user", "content": "Thanks, I am starting the Postgres setup now."}
        ],
        "manas@gmail.com": [
            {"role": "assistant", "content": "Hello Manas! I see you've completed your basic profile. Have you installed your IDE yet?"},
            {"role": "user", "content": "Yes, VS Code is working fine."},
            {"role": "assistant", "content": "Great. Your next step is to clone the main repository. Do you have GitHub access?"},
            {"role": "user", "content": "I tried to clone but got an access denied error. Can you help?"},
            {"role": "assistant", "content": "It seems your GitHub handle isn't joined to the organization. Please go to the Access Request portal at `access.internal.io` and submit a ticket for the 'Frontend MonoRepo', then let me know once approved."}
        ],
        "archit@gmail.com": [
            {"role": "assistant", "content": "Hi Archit, welcome aboard! Are you ready to dive into the technical setup?"},
            {"role": "user", "content": "Hey! Yes, I've got my laptop running and terminal configured."},
            {"role": "assistant", "content": "Perfect. You have two technical tasks: getting AWS CLI credentials and setting up the staging Redis endpoint."},
            {"role": "user", "content": "I'm done with both. The AWS credentials test was successful, and I connected to Redis over the VPN."},
            {"role": "assistant", "content": "Excellent speed! Let's move on to Security Training. Next task is the Data Privacy Modules. Watch the 15-minute video and click done."},
            {"role": "user", "content": "Just watched it. It's done."},
            {"role": "assistant", "content": "Great job. Next up is the compliance quiz. The link is in your inbox."}
        ]
    }

    try:
        for email, logs in targets.items():
            user = db.query(User).filter(User.email == email).first()
            if not user:
                print(f"Skipping {email}: User not found in database.")
                continue

            session = db.query(OnboardingSession).filter(OnboardingSession.user_id == user.id).first()
            if not session:
                print(f"Skipping {email}: No onboarding session found.")
                continue

            # Clear existing logs for this session to make script idempotent
            deleted = db.query(ConversationLog).filter(ConversationLog.session_id == session.id).delete()
            if deleted > 0:
                print(f"Cleared {deleted} existing chat logs for {email}.")

            # Insert new logs with realistic incrementing timestamps ending near 'now'
            start_time = datetime.utcnow() - timedelta(minutes=len(logs)*10)
            
            for index, log in enumerate(logs):
                msg_time = start_time + timedelta(minutes=index*8) # space out messages
                
                chat_msg = ConversationLog(
                    session_id=session.id,
                    role=log["role"],
                    content=log["content"],
                    created_at=msg_time
                )
                db.add(chat_msg)
            
            print(f"Successfully seeded {len(logs)} messages for {email}.")

        db.commit()
        print("Database commit successful. All dummy chat histories injected.")

    except Exception as e:
        db.rollback()
        print(f"Error during seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_chat_logs()
