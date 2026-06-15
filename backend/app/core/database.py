import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# CRITICAL FIX: Force FastAPI to read the .env file and ignore Windows cache
load_dotenv(override=True)

logger = logging.getLogger(__name__)

# Bypass the cached settings object to guarantee we get the fresh .env value
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Fallback just in case dotenv fails to find it
if not SQLALCHEMY_DATABASE_URL:
    from app.core.config import settings
    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Make sure it crashes loudly if the URL is missing, rather than failing silently on localhost
if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL is missing from environment variables!")

connected_host = SQLALCHEMY_DATABASE_URL.split('@')[-1].split('/')[0] if '@' in SQLALCHEMY_DATABASE_URL else 'local'
logger.info(f"Connecting to database at: {connected_host}")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    FastAPI dependency that provides a local database session for a single request.
    Ensures the session is closed after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()