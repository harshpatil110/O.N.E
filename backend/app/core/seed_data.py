from sqlalchemy.orm import Session
from app.core.security import hash_password

# Import the User model here. If missing, assume app.models.user is where it will be placed.
try:
    from app.models.user import User
except ImportError:
    pass

def seed_users(db: Session):
    """
    Seed test users.
    Creates an HR Admin and a regular employee.
    """
    # Create one HR admin user
    hr_admin = User(
        name="HR Admin",
        email="hr@company.com",
        hashed_password=hash_password("adminpassword123"),
        role="hr_admin"
    )
    
    # Create one test employee
    employee = User(
        name="Test Developer",
        email="dev@company.com",
        hashed_password=hash_password("devpassword123"),
        role="employee"
    )
    
    db.add_all([hr_admin, employee])
    db.commit()
    print("Seeded test users successfully!")

if __name__ == "__main__":
    from app.core.database import SessionLocal
    db = SessionLocal()
    try:
        seed_users(db)
    finally:
        db.close()
