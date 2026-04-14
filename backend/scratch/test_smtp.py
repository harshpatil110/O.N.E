import sys
import os
from unittest.mock import MagicMock
import asyncio

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from dotenv import load_dotenv
load_dotenv()

from app.services.email_service import EmailService
from app.services.email_template import generate_completion_email_html

async def test_email_send():
    print("Testing Email Service...")
    service = EmailService()
    
    # Mock user and session for template
    user = MagicMock()
    user.name = "Test Developer"
    user.email = os.getenv("HR_EMAIL") # Send to yourself for test
    user.role = "Senior Backend Engineer"
    user.created_at = None 
    
    session = MagicMock()
    session.id = "test-session-uuid"
    session.persona = {"team": "Platform", "tech_stack": ["Python", "FastAPI"]}
    
    # Mock checklist items
    item1 = MagicMock()
    item1.title = "Setup Environment"
    item1.status = "completed"
    
    item2 = MagicMock()
    item2.title = "Security Training"
    item2.status = "pending"
    
    checklist = [item1, item2]
    
    html = generate_completion_email_html(user, session, checklist, 50, 2.5)
    
    print(f"Sending test email to {user.email}...")
    success = service.send_email(
        to=user.email,
        subject="🚀 O.N.E. SMTP Validation Test",
        html_body=html
    )
    
    if success:
        print("✅ Email sent successfully!")
    else:
        print("❌ Email sending failed.")

if __name__ == "__main__":
    asyncio.run(test_email_send())
