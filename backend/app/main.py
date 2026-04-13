from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.auth import router as auth_router
from app.api.onboarding import router as onboarding_router
from app.api.checklist import router as checklist_router

app = FastAPI(title="O.N.E API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
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
