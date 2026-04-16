from fastapi import APIRouter, HTTPException, Path as FastAPIPath
from fastapi.responses import PlainTextResponse
from typing import List, Dict, Any
from app.services.docs_service import get_all_docs, get_doc_content

router = APIRouter(prefix="/docs", tags=["Documentation"])

@router.get("", response_model=List[Dict[str, Any]])
async def list_documents():
    """Returns the structured JSON list of categories and available articles."""
    try:
        return get_all_docs()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{filename:path}")
async def get_document(filename: str):
    """Returns the raw Markdown string for that specific file."""
    try:
        # Utilizing PlainTextResponse for a raw string return
        content = get_doc_content(filename)
        return PlainTextResponse(content)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
