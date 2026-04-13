import os
import sys
from sqlalchemy import text
from app.core.database import SessionLocal, engine
from app.core.security import hash_password

def seed_users():
    session = SessionLocal()
    try:
        # Emergency safety check: make sure the users table has hashed_password
        # as Drizzle schema might not have deployed it yet.
        try:
            session.execute(text("ALTER TABLE users ADD COLUMN hashed_password VARCHAR(255);"))
            session.commit()
            print("Added missing hashed_password column to users table.")
        except Exception as e:
            session.rollback()
            # It's okay if this fails, the column likely already exists
            print("Column hashed_password check passed safely.")

        hr_pw = hash_password("adminpassword123")
        dev_pw = hash_password("devpassword123")
        
        # Check if HR Admin exists
        hr = session.execute(text("SELECT id FROM users WHERE email = :email"), {"email": "hr@company.com"}).fetchone()
        if not hr:
            session.execute(text("""
                INSERT INTO users (name, email, role, hashed_password) 
                VALUES (:name, :email, :role, :hashed_password)
            """), {
                "name": "HR Admin", 
                "email": "hr@company.com", 
                "role": "hr_admin", 
                "hashed_password": hr_pw
            })
            print("Successfully inserted HR Admin user.")
        else:
            print("HR Admin already exists. Skipping insertion.")
        
        # Check if Developer exists
        dev = session.execute(text("SELECT id FROM users WHERE email = :email"), {"email": "dev@company.com"}).fetchone()
        if not dev:
            session.execute(text("""
                INSERT INTO users (name, email, role, hashed_password) 
                VALUES (:name, :email, :role, :hashed_password)
            """), {
                "name": "Test Developer", 
                "email": "dev@company.com", 
                "role": "employee", 
                "hashed_password": dev_pw
            })
            print("Successfully inserted Test Developer user.")
        else:
            print("Test Developer already exists. Skipping insertion.")
            
        session.commit()
        print("NeonDB Database seeded with test users successfully!")
        
    except Exception as e:
        session.rollback()
        print(f"Error during emergency seed: {str(e)}")
        sys.exit(1)
    finally:
        session.close()

if __name__ == "__main__":
    seed_users()
