import os
from dotenv import load_dotenv

# 1. Force the environment variables to update BEFORE anything else
load_dotenv(override=True)
db_url = os.getenv("DATABASE_URL")

print(f"Targeting Database: {db_url.split('@')[-1] if db_url and '@' in db_url else 'INVALID URL'}")

# 2. Import SQLAlchemy and your models
from sqlalchemy import create_engine
from app.core.database import Base
from app.models.user import User
from app.models.onboarding_session import OnboardingSession
from app.models.conversation_log import ConversationLog
# Add any other models you have here (e.g., from app.models.task import Task)

# 3. Create a direct engine to Supabase and force the table creation
try:
    print("Building tables...")
    engine = create_engine(db_url)
    Base.metadata.create_all(bind=engine)
    print("SUCCESS! All tables have been built in Supabase.")
except Exception as e:
    print(f"FAILED: {e}")