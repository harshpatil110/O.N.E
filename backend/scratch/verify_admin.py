import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.getcwd(), '.env'))

from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import create_access_token

client = TestClient(app)

def run_tests():
    db = SessionLocal()
    
    dev_user = db.query(User).filter_by(email="dev@company.com").first()
    hr_user = db.query(User).filter_by(email="hr@company.com").first()

    if not dev_user:
        dev_user = db.query(User).filter_by(role="employee").first()
        print(f"Warning: dev@company.com not found, using {dev_user.email} instead")

    if not hr_user:
        hr_user = db.query(User).filter_by(role="hr_admin").first()
        print(f"Warning: hr@company.com not found, using {hr_user.email} instead")

    if not dev_user or not hr_user:
        print("Required users not found in DB! Seed your database first.")
        return

    print(f"Found Dev User: {dev_user.email} (Role: {dev_user.role})")
    print(f"Found HR User: {hr_user.email} (Role: {hr_user.role})")

    # Create tokens for testing
    dev_token = create_access_token(data={"sub": str(dev_user.id), "role": dev_user.role})
    hr_token = create_access_token(data={"sub": str(hr_user.id), "role": hr_user.role})

    print("\n[TEST 1] Accessing /api/v1/admin/metrics with Dev User")
    response_dev = client.get(
        "/api/v1/admin/metrics", 
        headers={"Authorization": f"Bearer {dev_token}"}
    )
    print(f"Status Code: {response_dev.status_code}")
    print(f"Response: {response_dev.json()}")
    if response_dev.status_code == 403:
        print("Passed: Correctly returned 403 Forbidden\n")
    else:
        print("Failed: Did not return 403 Forbidden\n")


    print("[TEST 2] Accessing /api/v1/admin/metrics with HR User")
    response_hr = client.get(
        "/api/v1/admin/metrics", 
        headers={"Authorization": f"Bearer {hr_token}"}
    )
    print(f"Status Code: {response_hr.status_code}")
    if response_hr.status_code == 200:
        print(f"Metrics: {response_hr.json()}")
        print("Passed: Correctly returned 200 OK and Metrics Data\n")
    else:
        print(f"Response: {response_hr.json()}")
        print("Failed: Did not return 200 OK\n")

if __name__ == "__main__":
    run_tests()
