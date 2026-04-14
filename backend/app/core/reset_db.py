import os
import sys

# Ensure the app module can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.core.database import engine, Base
# Import all models so SQLAlchemy knows about them before creating tables
from app.models.user import User
from app.models.onboarding_session import OnboardingSession
from app.models.checklist_template import ChecklistTemplate
from app.models.checklist_item import ChecklistItem
from app.models.conversation_log import ConversationLog

def reset_database():
    print("⚠️ Dropping all existing tables...")
    Base.metadata.drop_all(bind=engine)
    
    print("🏗️ Recreating tables with the latest schema...")
    Base.metadata.create_all(bind=engine)
    
    print("✅ Database successfully reset! The 'tool_name' column now exists.")

if __name__ == "__main__":
    reset_database()