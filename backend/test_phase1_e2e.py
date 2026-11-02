import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.user import User
from app.models.developer_task_state import DeveloperTaskState
from app.models.completed_checklist_item import CompletedChecklistItem

client = TestClient(app)

def run_e2e_verification():
    print("=" * 70)
    print("      PHASE 1 END-TO-END VERIFICATION TEST")
    print("=" * 70)

    # 1. Setup a test developer user & active task in DB
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == "demo_tester@nexusai.dev").first()
        if not user:
            from app.core.security import hash_password
            user = User(
                name="Demo Tester",
                email="demo_tester@nexusai.dev",
                hashed_password=hash_password("password123"),
                role="employee",
                department_role="backend dev",
                onboarding_progress=0.0
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Clean existing test task states
        db.query(DeveloperTaskState).filter(DeveloperTaskState.user_id == user.id).delete()
        db.commit()

        # Create active task
        active_task = DeveloperTaskState(
            user_id=user.id,
            task_sequence_number=1,
            task_name="Configure PostgreSQL & Execute Alembic Migrations",
            status="active"
        )
        db.add(active_task)
        db.commit()
        db.refresh(active_task)
        task_id = active_task.id
        print(f"Created active test task: ID={task_id}, Name='{active_task.task_name}' for {user.email}")

        # 2. Test GET /tasks/{task_id}/checklist-items (Auto-generates subtasks)
        print("\n--- TEST: GET /tasks/{task_id}/checklist-items ---")
        get_res = client.get(f"/tasks/{task_id}/checklist-items?user_email={user.email}")
        assert get_res.status_code == 200, f"GET failed: {get_res.text}"
        data = get_res.json()
        print(f"Task ID: {data['task_id']}")
        print(f"Overall Confidence: {data['overall_confidence']}% ({data['confidence_label']})")
        print(f"Subtasks Generated: {len(data['items'])}")
        assert data['overall_confidence'] == 85.0
        assert data['confidence_label'] == "Good Confidence"
        assert len(data['items']) == 4

        # 3. Test POST /tasks/submit with Proof-of-Work upload
        print("\n--- TEST: POST /tasks/submit with Proof-of-Work ---")
        proof_payload = {
            "task_id": task_id,
            "github_repo_url": "https://github.com/nexusai/one-capstone/pull/42",
            "proof_notes": "Alembic migrations completed successfully: target head 8f4a12c.\nSwagger /docs returns 200 OK.",
            "screenshots": [
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==",
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
            ]
        }
        submit_res = client.post("/tasks/submit", json=proof_payload)
        assert submit_res.status_code == 200, f"Submit failed: {submit_res.text}"
        submit_data = submit_res.json()
        print("Submit Response:", submit_data)
        assert submit_data["status"] == "success"

        # 4. Verify Task State transitioned in DB
        db.refresh(active_task)
        print(f"Active task status in DB: '{active_task.status}'")
        assert active_task.status == "pending_verification"
        print(f"AI speed analysis: '{active_task.speed_analysis}'")
        print(f"AI learning curve: '{active_task.learning_curve}'")
        print(f"AI mistakes made:  '{active_task.mistakes_made}'")

        # 5. Verify CompletedChecklistItem records in DB
        saved_items = db.query(CompletedChecklistItem).filter(
            CompletedChecklistItem.task_id == task_id
        ).order_by(CompletedChecklistItem.subtask_number.asc()).all()

        print(f"\nPersisted CompletedChecklistItems in DB: {len(saved_items)}")
        for item in saved_items:
            has_screenshot = "YES (Base64)" if item.screenshot_data else "NO"
            print(f"  [{item.subtask_number}] {item.subtask_title}")
            print(f"      Tier: {item.verification_tier} | Weight: {item.weight_score}% | Type: {item.proof_type}")
            print(f"      Proof: {item.proof_text[:60] if item.proof_text else 'None'} | Screenshot: {has_screenshot}")

        # Subtask 1 should have the github link and screenshot 1
        assert saved_items[0].proof_text == proof_payload["github_repo_url"]
        assert saved_items[0].screenshot_data == proof_payload["screenshots"][0]

        # 6. Re-query GET /api/v1/tasks/{task_id}/checklist-items to verify updated items
        print("\n--- TEST: GET /api/v1/tasks/{task_id}/checklist-items after submit ---")
        get_after = client.get(f"/api/v1/tasks/{task_id}/checklist-items")
        assert get_after.status_code == 200
        after_data = get_after.json()
        assert after_data["overall_confidence"] == 85.0
        assert after_data["items"][0]["proof_text"] == proof_payload["github_repo_url"]
        assert after_data["items"][0]["screenshot_data"] == proof_payload["screenshots"][0]
        print("Verified: GET returns the exact persisted 6-Tier subtasks and screenshot data!")

        print("\n" + "=" * 70)
        print("  ALL PHASE 1 END-TO-END VERIFICATION CHECKS PASSED 100%!")
        print("=" * 70)

    finally:
        db.close()

if __name__ == "__main__":
    run_e2e_verification()

