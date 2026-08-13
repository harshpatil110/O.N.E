import os
import sys
import httpx

# Add backend dir to path for DB imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import SessionLocal
from app.models.user import User

API_URL = "http://localhost:8000/api/v1"

def reset_harsh():
    with SessionLocal() as db:
        user = db.query(User).filter(User.email == "harsh123@gmail.com").first()
        if user:
            user.onboarding_progress = 0
            user.tasks_completed = 0
            user.department_role = None
            db.commit()

def login(email: str, password: str = "defaultpassword123") -> str:
    with httpx.Client() as client:
        res = client.post(f"{API_URL}/auth/login", json={"email": email, "password": password})
        if res.status_code != 200:
            print(f"Login failed: {res.text}")
            return None
        return res.json()["access_token"]

def test_harsh_flow_0_percent_gate():
    """
    Action 10.1 (Harsh's Flow): 0% progress onboarding gate test.
    """
    reset_harsh()
    token = login("harsh123@gmail.com")
    assert token, "Login for harsh123 failed"
    
    headers = {"Authorization": f"Bearer {token}"}
    
    with httpx.Client(headers=headers, timeout=120.0) as client:
        # Start Session
        start_res = client.post(f"{API_URL}/onboarding/start")
        assert start_res.status_code == 200, f"Start session failed: {start_res.text}"
        session_id = start_res.json()["session_id"]
        
        # Send Chat Message
        chat_res = client.post(f"{API_URL}/chat/{session_id}/message", json={"message": "hello"})
        assert chat_res.status_code == 200, f"Chat failed: {chat_res.text}"
        
        reply = chat_res.json()["content"].lower()
        print(f"\n[Harsh's Reply (0% Gate)]: {reply}")
        
        assert "name" in reply or "what's your" in reply or "what is your" in reply, "Did not hit the 0% onboarding gate"

def test_manas_flow_task_trigger():
    """
    Action 10.2 (Manas's Flow): Task fetching NLP tool trigger test.
    """
    token = login("manas123@gmail.com")
    assert token, "Login for manas123 failed"
    
    headers = {"Authorization": f"Bearer {token}"}
    
    with httpx.Client(headers=headers, timeout=120.0) as client:
        # Start Session
        start_res = client.post(f"{API_URL}/onboarding/start")
        assert start_res.status_code == 200, f"Start session failed: {start_res.text}"
        session_id = start_res.json()["session_id"]
        
        # Send Chat Message
        chat_res = client.post(f"{API_URL}/chat/{session_id}/message", json={"message": "What is my next task?"})
        assert chat_res.status_code == 200, f"Chat failed: {chat_res.text}"
        
        reply = chat_res.json()["content"].lower()
        print(f"\n[Manas's Reply (Task Tool)]: {reply}")
        
        assert "task" in reply, "Agent did not mention the task"

if __name__ == "__main__":
    print("Running E2E Agent Tests...")
    test_harsh_flow_0_percent_gate()
    test_manas_flow_task_trigger()
    print("\nAll tests passed!")
