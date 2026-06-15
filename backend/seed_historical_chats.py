import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# Override environment to ensure we connect to Supabase
load_dotenv(override=True)

from app.core.database import SessionLocal
from app.models.user import User
from app.models.onboarding_session import OnboardingSession
from app.models.conversation_log import ConversationLog

# Realistic chat transcripts customized by developer
# Format: list of (role, content, minutes_offset_from_start)
TRANSCRIPTS = {
    "parth@gmail.com": [
        ("assistant", "Welcome to O.N.E., Parth! Let's get your Data Engineering environment set up. First, do you have Postgres installed locally?", 0),
        ("user", "Hi! Yes, I have Postgres installed, but I need help with the local setup and seeding the databases.", 5),
        ("assistant", "Great. You'll find the initialization scripts in the `data-infra/scripts` repository. Run `./init-local-db.sh` to get started. Do you have access to that repo?", 6),
        ("user", "Let me check... Ah, I don't think I have access to `data-infra` yet. I get a 404 on GitHub.", 10),
        ("assistant", "No problem. I've automatically requested GitHub access for you. While we wait, let's configure your AWS credentials. Please check your email for the SSO login link.", 11),
        ("user", "Okay, I got the email and logged into AWS SSO. What's the next step?", 45),
        ("assistant", "Excellent. Now install the AWS CLI and run `aws configure sso`. Use `us-east-1` as your default region.", 46),
        ("user", "Done! It says I am logged in as a data-engineer-role.", 52),
        ("assistant", "Perfect. Let's move on to setting up your Apache Airflow environment. Please pull the `airflow-dags` repository...", 53),
    ],
    "manas@gmail.com": [
        ("assistant", "Hello Manas! Welcome aboard. Let's set up your Frontend Engineering workspace. First, let's clone the main React repository.", 0),
        ("user", "Hey! Cloning it now. Should I use npm or yarn?", 2),
        ("assistant", "We use `pnpm` exclusively in our frontend projects. Please install it globally with `npm i -g pnpm`, then run `pnpm install` in the project root.", 3),
        ("user", "Alright, pnpm install is running. By the way, where can I find the Figma design files?", 15),
        ("assistant", "The Figma project is linked in your welcome email. You should already have Editor access. Let me know if you can't access it.", 16),
        ("user", "Found it, thanks! The pnpm install finished. I'm getting an error when I run `pnpm dev` though. Something about a missing `.env` file?", 22),
        ("assistant", "Ah, you need to copy the example environment file. Run `cp .env.example .env.local`. It contains the mock API endpoints for local development.", 23),
        ("user", "That fixed it, the dev server is up! The app looks great locally. What's my first task?", 30),
        ("assistant", "Awesome! Your first task is to review the component library documentation in Storybook. Run `pnpm storybook` to start it up.", 31),
    ],
    "archit@gmail.com": [
        ("assistant", "Welcome to O.N.E., Archit! Let's kick off your Backend Engineering onboarding. We'll start with the FastAPI services.", 0),
        ("user", "Hi there. Looking forward to it. I've cloned the `core-api` repo. What version of Python are we using?", 10),
        ("assistant", "We use Python 3.12. We recommend using `pyenv` to manage Python versions. Let's set up a virtual environment.", 11),
        ("user", "Okay, I've created the venv and activated it. Should I pip install requirements.txt?", 25),
        ("assistant", "We use `poetry` for dependency management. Please install poetry, and then run `poetry install` in the project directory.", 26),
        ("user", "Poetry installed and dependencies are resolving. What about the database? Do I need Docker?", 40),
        ("assistant", "Yes, we use Docker Compose for local dependencies (Postgres, Redis). Run `docker-compose up -d` in the `infra/local` directory.", 41),
        ("user", "Docker containers are up. How do I run the database migrations?", 55),
        ("assistant", "Run `alembic upgrade head`. After that, you can start the development server with `fastapi dev app/main.py`.", 56),
    ]
}

def seed_transcripts():
    db = SessionLocal()
    try:
        print("[1/3] Identifying users and sessions...")
        users = db.query(User).filter(User.email.in_(TRANSCRIPTS.keys())).all()
        
        if not users:
            print("No matching users found.")
            return

        for user in users:
            session = db.query(OnboardingSession).filter(OnboardingSession.user_id == user.id).first()
            if not session:
                print(f"Skipping {user.email}: No active onboarding session.")
                continue
                
            print(f"[2/3] Cleaning old logs for {user.email}...")
            # Delete any existing conversation logs for this session to avoid duplicates
            old_logs = db.query(ConversationLog).filter(ConversationLog.session_id == session.id).all()
            for log in old_logs:
                db.delete(log)
            db.commit()

            print(f"[3/3] Injecting rich conversation for {user.email}...")
            transcript = TRANSCRIPTS[user.email]
            
            # Start the conversation 2 days ago
            base_time = datetime.now(timezone.utc) - timedelta(days=2)
            
            for role, content, minutes_offset in transcript:
                log_time = base_time + timedelta(minutes=minutes_offset)
                
                new_log = ConversationLog(
                    session_id=session.id,
                    role=role,
                    content=content,
                    created_at=log_time
                )
                db.add(new_log)
                
            db.commit()
            print(f"  [OK] Successfully seeded {len(transcript)} messages for {user.email}.")
            
        print("\n[DONE] Historical chat seeding completed successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding historical chats: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_transcripts()
