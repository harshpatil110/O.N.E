from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Google Gemini API
    GEMINI_API_KEY: str

    # PostgreSQL
    DATABASE_URL: str

    # JWT Auth
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_MINUTES: int = 480

    # Gmail SMTP
    GMAIL_ADDRESS: str
    GMAIL_APP_PASSWORD: str

    # HR Email
    HR_EMAIL: str

    # ChromaDB
    CHROMA_PERSIST_DIRECTORY: str = "./chroma_db"
    CHROMA_COLLECTION_NAME: str = "one_knowledge_base"

    # App
    APP_ENV: str = "development"
    FRONTEND_URL: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
