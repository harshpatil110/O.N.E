import os
import sys
from dotenv import load_dotenv

# Force environment variables
load_dotenv(override=True)

# Add root directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.user import User
from app.models.onboarding_session import OnboardingSession

def seed_users():
    db = SessionLocal()
    print("Connecting to Supabase to create users...")

    # The exact users your chat script is looking for
    demo_users = [
        {"email": "parth@gmail.com", "name": "Parth Shah", "role": "Data Engineer"},
        {"email": "manas@gmail.com", "name": "Manas Gupta", "role": "Frontend Engineer"},
        {"email": "archit@gmail.com", "name": "Archit Verma", "role": "Backend Engineer"}
    ]

    try:
        for u in demo_users:
            # 1. Check if user exists, if not create them
            user = db.query(User).filter(User.email == u["email"]).first()
            if not user:
                user = User(
                    email=u["email"], 
                    name=u["name"], 
                    hashed_password="hashed_demo_password", # Just a dummy password
                    role=u["role"]
                )
                db.add(user)
                db.commit()
                db.refresh(user)
                print(f"✅ Created User: {user.name}")
            else:
                print(f"User {u['name']} already exists.")

            # 2. Give them an active onboarding session so the chat logs have a place to attach
            session = db.query(OnboardingSession).filter(OnboardingSession.user_id == user.id).first()
            if not session:
                session = OnboardingSession(user_id=user.id)
                db.add(session)
                db.commit()
                print(f"✅ Created Onboarding Session for: {user.name}")

        print("\nAll prerequisite users created successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_users()