from typing import Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.rag.ingest import ingest_knowledge_base
from app.rag.rag_service import RAGService

router = APIRouter()

class KnowledgeQueryRequest(BaseModel):
    query: str
    role: Optional[str] = None
    category: Optional[str] = None

# Dummy or existing dependency for user checking
def get_admin_user():
    return {"user": "admin"}

def get_current_user():
    return {"user": "current_user"}

@router.post("/knowledge/ingest")
async def trigger_ingestion(current_user: dict = Depends(get_admin_user)):
    """
    Triggers the knowledge base ingestion pipeline to parse Markdown files and store embeddings.
    """
    await ingest_knowledge_base()
    return {"status": "ingestion complete"}

@router.post("/knowledge/query")
async def query_knowledge_base(
    request: KnowledgeQueryRequest,
    current_user: dict = Depends(get_current_user)
):
    rag = RAGService()
    results = await rag.retrieve(
        query=request.query,
        role=request.role,
        category=request.category
    )
    return {"query": request.query, "results": results}
