import os
import asyncio
import sys
import logging
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the parent directory to sys.path to allow absolute imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.rag.document_loader import load_knowledge_base
from app.rag.chunker import chunk_documents
from app.rag.chroma_client import get_collection
from app.rag.embeddings import NvidiaEmbeddingFunction

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def ingest_knowledge_base(kb_directory: Optional[str] = None):
    """
    Full ingestion pipeline:
    1. Load all documents from knowledge_base/
    2. Chunk them
    3. Generate embeddings via Gemini
    4. Store in ChromaDB
    
    Idempotent: clears existing collection and rebuilds from scratch.
    """
    if kb_directory is None:
        # Resolve path to ../../knowledge_base relative to this file
        current_dir = os.path.dirname(__file__)
        kb_directory = os.path.abspath(os.path.join(current_dir, "../../knowledge_base"))
    
    logger.info(f"Loading documents from: {kb_directory}")
    documents = load_knowledge_base(kb_directory)
    logger.info(f"Loaded {len(documents)} documents")
    
    if not documents:
        logger.warning("No documents found. Skipping ingestion.")
        return
        
    logger.info("Chunking documents...")
    chunks = chunk_documents(documents)
    logger.info(f"Created {len(chunks)} chunks")
    
    logger.info("Storing in ChromaDB...")
    collection = get_collection()
    embedding_fn = NvidiaEmbeddingFunction()
    
    # Process in batches of 10 to respect rate limits
    batch_size = 10
    total_batches = (len(chunks) - 1) // batch_size + 1
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        
        # Prepare metadata for ChromaDB (values must be str, int, float, or bool)
        clean_metadatas = []
        for c in batch:
            clean_meta = {}
            for k, v in c["metadata"].items():
                if isinstance(v, list):
                    # Convert list of strings to a comma-separated string
                    clean_meta[k] = ",".join([str(item) for item in v])
                elif v is None:
                    continue
                else:
                    clean_meta[k] = v
            clean_metadatas.append(clean_meta)

        collection.upsert(
            ids=[c["id"] for c in batch],
            documents=[c["content"] for c in batch],
            metadatas=clean_metadatas,
            embeddings=embedding_fn([c["content"] for c in batch])
        )
        logger.info(f"  Ingested batch {i//batch_size + 1}/{total_batches}")
    
    logger.info(f"Ingestion complete. Total chunks in collection: {collection.count()}")

if __name__ == "__main__":
    asyncio.run(ingest_knowledge_base())
