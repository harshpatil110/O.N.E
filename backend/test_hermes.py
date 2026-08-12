import os
import sys
import asyncio
from dotenv import load_dotenv

# Load env variables
load_dotenv(override=True)

# Ensure app imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.onboarding_session import OnboardingSession

def main():
    db = SessionLocal()
    session = db.query(OnboardingSession).first()
    
    if session:
        print(f"Session ID: {session.id}")
        
        # Test agent execution
        import asyncio
        from app.core.agent import run_hermes_agent
        
        async def run_test():
            msg = "What is our PTO policy?"
            history = []
            
            print(f"Querying Agent: {msg}")
            reply = await run_hermes_agent(msg, history)
            print(f"\nAgent Response:\n{reply}")
            
        asyncio.run(run_test())
    else:
        print("No sessions found.")

if __name__ == "__main__":
    main()
