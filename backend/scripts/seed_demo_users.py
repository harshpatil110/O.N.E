import sys
import os

# Ensure backend directory is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import hash_password


def seed_demo_users():
    db = SessionLocal()
    try:
        print("--- Starting Demo User Seeding ---")

        # 1. Wipe existing users except Master Admin (patilha2005@gmail.com)
        admin_email = "patilha2005@gmail.com"
        deleted_count = (
            db.query(User)
            .filter(User.email != admin_email)
            .delete(synchronize_session=False)
        )
        db.commit()
        print(f"Deleted {deleted_count} existing non-admin user(s). Preserved admin: {admin_email}")

        # Ensure Master Admin exists if missing
        admin_user = db.query(User).filter(User.email == admin_email).first()
        if not admin_user:
            admin_user = User(
                name="Master Admin",
                email=admin_email,
                hashed_password=hash_password("123456"),
                role="admin",
                department_role="IT",
                tasks_completed=0,
                onboarding_progress=100.0,
            )
            db.add(admin_user)
            db.commit()
            print(f"Created Master Admin account: {admin_email}")

        # 2. Hash password "123456"
        hashed_pw = hash_password("123456")

        # 3. Target demo users
        demo_users_data = [
            {
                "name": "Archit Chitte",
                "email": "archit123@gmail.com",
                "role": "employee",
                "department_role": "frontend dev",
                "tasks_completed": 6,
                "onboarding_progress": 30.0,
            },
            {
                "name": "Parth Narkar",
                "email": "parth123@gmail.com",
                "role": "employee",
                "department_role": "database dev",
                "tasks_completed": 15,
                "onboarding_progress": 75.0,
            },
            {
                "name": "Manas Patil",
                "email": "manas123@gmail.com",
                "role": "employee",
                "department_role": "backend dev",
                "tasks_completed": 10,
                "onboarding_progress": 50.0,
            },
            {
                "name": "Harsh Patil",
                "email": "harsh123@gmail.com",
                "role": "employee",
                "department_role": "AI dev",
                "tasks_completed": 0,
                "onboarding_progress": 0.0,
            },
        ]

        for user_data in demo_users_data:
            user = User(
                name=user_data["name"],
                email=user_data["email"],
                hashed_password=hashed_pw,
                role=user_data["role"],
                department_role=user_data["department_role"],
                tasks_completed=user_data["tasks_completed"],
                onboarding_progress=user_data["onboarding_progress"],
            )
            db.add(user)
            print(
                f"Seeded: {user_data['name']} ({user_data['email']}) | "
                f"Dept Role: {user_data['department_role']} | "
                f"Tasks Completed: {user_data['tasks_completed']} | "
                f"Progress: {user_data['onboarding_progress']}%"
            )

        db.commit()
        print("--- Seeding Completed Successfully ---")

        # 4. Assertions & Validation
        all_users = db.query(User).all()
        user_count = len(all_users)
        print(f"\n[VALIDATION] Total Users in Database: {user_count}")

        harsh_user = db.query(User).filter(User.email == "harsh123@gmail.com").first()
        if harsh_user:
            print(
                f"[VALIDATION] harsh123@gmail.com tasks_completed: {harsh_user.tasks_completed} "
                f"(Expected: 0), progress: {harsh_user.onboarding_progress}%"
            )

        assert user_count == 5, f"Expected 5 users, found {user_count}"
        assert (
            harsh_user and harsh_user.tasks_completed == 0
        ), "harsh123@gmail.com should have 0 tasks completed"

        print("[SUCCESS] All database assertions PASSED 100%!")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Seeding failed: {e}")
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_users()
