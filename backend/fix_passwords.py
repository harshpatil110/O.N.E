import os
import sys
import bcrypt
from dotenv import load_dotenv

# Force environment variables
load_dotenv(override=True)

# Add root directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.user import User

def hash_password(password: str) -> str:
    """Generates a real, valid bcrypt hash."""
    salt = bcrypt.gensalt()
    # Hash the password and decode it back to a string for the database
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def fix_database_passwords():
    db = SessionLocal()
    print("Connecting to Supabase to fix passwords...")

    # The password you will type into the frontend UI to log in
    plain_text_password = "123456"
    real_hash = hash_password(plain_text_password)

    try:
        # Get all users and update their password to the real hash
        users = db.query(User).all()
        for user in users:
            user.hashed_password = real_hash
            print(f"✅ Repaired password for: {user.email}")
            
        db.commit()
        print(f"\nSUCCESS! All users can now log in using the password: {plain_text_password}")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    fix_database_passwords()