import chromadb
from chromadb.config import Settings
import os

def get_chroma_client():
    persist_dir = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
    return chromadb.PersistentClient(
        path=persist_dir,
        settings=Settings(anonymized_telemetry=False)
    )

def get_collection(client=None):
    if client is None:
        client = get_chroma_client()
    return client.get_or_create_collection(
        name=os.getenv("CHROMA_COLLECTION_NAME", "one_knowledge_base"),
        metadata={"hnsw:space": "cosine"}
    )
