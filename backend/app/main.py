from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.auth import router as auth_router
from app.api.onboarding import router as onboarding_router
from app.api.checklist import router as checklist_router
from app.api.chat import router as chat_router
from app.api.admin import router as admin_router
from app.api.docs import router as docs_router
from app.api.analytics import router as analytics_router
from app.api.tasks import router as tasks_router

app = FastAPI(title="O.N.E API", version="1.0.0")

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:5175",
    settings.FRONTEND_URL,  # Keep the .env value as a fallback
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "O.N.E Backend"}

app.include_router(auth_router, prefix="/api/v1")
app.include_router(onboarding_router, prefix="/api/v1")
app.include_router(checklist_router, prefix="/api/v1")
app.include_router(chat_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")
app.include_router(docs_router, prefix="/api/v1")
app.include_router(analytics_router, prefix="/api/v1")
app.include_router(tasks_router, prefix="/api/v1")
