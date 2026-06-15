import os
from dotenv import load_dotenv

# Ensure we grab the live Supabase URL and bypass any Windows caching
load_dotenv(override=True)

import bcrypt
from app.core.database import SessionLocal
from app.models.user import User

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def seed_admin():
    db = SessionLocal()
    try:
        email = "patilha2005@gmail.com"
        password = "123456"
        role = "admin"
        name = "Master Admin"

        # Check if user already exists
        user = db.query(User).filter(User.email == email).first()

        if user:
            print(f"User {email} already exists. Updating password and role to admin.")
            user.hashed_password = hash_password(password)
            user.role = role
            user.name = name
        else:
            print(f"Creating new Master Admin account for {email}.")
            user = User(
                email=email,
                name=name,
                role=role,
                hashed_password=hash_password(password)
            )
            db.add(user)

        db.commit()
        print("Admin account successfully created or updated without IntegrityError!")

    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.close()
        print("Database session closed gracefully.")

if __name__ == "__main__":
    seed_admin()
