from fastapi import APIRouter, Depends
from app.rag.ingest import ingest_knowledge_base

router = APIRouter()

# Dummy or existing dependency for admin checking
def get_admin_user():
    return {"user": "admin"}

@router.post("/knowledge/ingest")
async def trigger_ingestion(current_user: dict = Depends(get_admin_user)):
    """
    Triggers the knowledge base ingestion pipeline to parse Markdown files and store embeddings.
    """
    await ingest_knowledge_base()
    return {"status": "ingestion complete"}
