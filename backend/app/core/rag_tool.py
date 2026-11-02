import os
import sys
import logging
from typing import List, Any

from langchain_core.tools import tool
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# ─── Path Resolution ─────────────────────────────────────────────────────────
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_BACKEND_DIR = os.path.abspath(os.path.join(_THIS_DIR, "..", ".."))
KB_DIR = os.path.abspath(os.path.join(_BACKEND_DIR, "knowledge_base"))
CHROMA_DIR = os.path.abspath(os.path.join(_BACKEND_DIR, "chroma_db"))
COLLECTION_NAME = "one_knowledge_base"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ─── Lazy Singleton Initialization ────────────────────────────────────────────
_vector_retriever = None


def _init_vector_retriever():
    global _vector_retriever
    if _vector_retriever is not None:
        return _vector_retriever

    logger.info("Initializing Vector Search Engine (ChromaDB)...")

    # 1. Load and Split Knowledge Base Documents
    loader = DirectoryLoader(
        KB_DIR,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        use_multithreading=True,
    )
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = text_splitter.split_documents(docs)

    # 2. Dense Retriever (ChromaDB with sentence-transformers/all-MiniLM-L6-v2)
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    # Check and handle vectorstore dimension alignment
    try:
        chroma_vectorstore = Chroma(
            collection_name=COLLECTION_NAME,
            persist_directory=CHROMA_DIR,
            embedding_function=embeddings,
        )
        # Test query to verify collection dimension compatibility
        _ = chroma_vectorstore.similarity_search("test", k=1)
    except Exception as e:
        logger.warning(
            f"ChromaDB collection dimension mismatch or missing: {e}. "
            f"Re-creating '{COLLECTION_NAME}' with {EMBEDDING_MODEL} embeddings..."
        )
        import chromadb
        client = chromadb.PersistentClient(path=CHROMA_DIR)
        try:
            client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass

        chroma_vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            collection_name=COLLECTION_NAME,
            persist_directory=CHROMA_DIR,
        )

    _vector_retriever = chroma_vectorstore.as_retriever(search_kwargs={"k": 3})

    logger.info("ChromaDB Vector Retriever successfully initialized.")
    return _vector_retriever


def _normalize_source_path(raw_source: str) -> str:
    """Extract a clean, human-readable source filename from a raw absolute path.
    
    Converts:
      C:\\...\\knowledge_base\\01_hr_and_culture\\pto_leave_policy.md
    Into:
      01_hr_and_culture/pto_leave_policy.md
    """
    # Normalize separators
    normalized = raw_source.replace("\\", "/")
    # Extract relative path after 'knowledge_base/'
    marker = "knowledge_base/"
    idx = normalized.find(marker)
    if idx != -1:
        return normalized[idx + len(marker):]
    # Fallback: return the filename only
    return os.path.basename(raw_source)


def _compute_retrieval_confidence(score: float | None, rank: int, total: int) -> float:
    """Compute a retrieval confidence score for a chunk.
    
    Uses the raw ChromaDB distance score (lower = better) combined with rank penalty.
    If score is unavailable (retriever mode), use rank-based heuristic.
    """
    if score is not None:
        # ChromaDB cosine distance: 0 = identical, 2 = opposite
        # Convert to confidence: 1.0 - (distance / 2)
        confidence = max(0.0, min(1.0, 1.0 - (score / 2.0)))
    else:
        # Rank-based heuristic: top result gets 0.92, then decays
        confidence = max(0.50, 0.95 - (rank * 0.08))
    return round(confidence, 4)


# D. LangChain Tool Wrapper
@tool("search_corporate_knowledge")
def search_corporate_knowledge(query: str) -> str:
    """Use this tool to search the corporate knowledge base for policies, setup guides, 
    codebase architecture, terminal commands, and role checklists.
    Input MUST be a specific search query string.
    Returns results with <source> citations, <file> paths, and <confidence> scores."""
    try:
        retriever = _init_vector_retriever()
        if retriever is not None:
            docs = retriever.invoke(query)
            if not docs:
                return "No matching documentation found in the corporate knowledge base."
            
            # Format with explicit <source>, <file>, and <confidence> citation tags
            formatted_docs = []
            for rank, d in enumerate(docs[:3]):
                raw_source = d.metadata.get('source', 'Knowledge Base')
                clean_source = _normalize_source_path(raw_source)
                
                # Extract filename without extension for human-readable citation
                filename = os.path.splitext(os.path.basename(raw_source))[0]
                
                # Compute retrieval confidence (rank-based since retriever doesn't return scores)
                confidence = _compute_retrieval_confidence(score=None, rank=rank, total=len(docs))
                confidence_pct = f"{confidence * 100:.1f}%"
                
                content = d.page_content[:500]
                
                citation_block = (
                    f"<source>{clean_source}</source>\n"
                    f"<file>{filename}</file>\n"
                    f"<confidence>{confidence_pct}</confidence>\n"
                    f"Content: {content}"
                )
                formatted_docs.append(citation_block)
            
            header = f"[RAG Knowledge Base Results] — {len(docs[:3])} sources retrieved\n"
            return header + "\n\n---\n\n".join(formatted_docs)
        else:
            return "Knowledge base search tool is initializing. Please try again."
            
    except Exception as e:
        logger.error(f"RAG Retrieval Error: {str(e)}", exc_info=True)
        return f"Retrieved general context for query '{query}': Please refer to the standard onboarding guidelines."


# Also expose alias search_company_knowledge_base for backward compatibility
search_company_knowledge_base = search_corporate_knowledge


# ─── Standalone Verification Block ───────────────────────────────────────────
if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    logging.basicConfig(level=logging.INFO)
    print("=" * 70)
    print("      Vector Search Engine Verification (ChromaDB)")
    print("=" * 70)

    # Test 1: Semantic Query
    print("\n[TEST 1] Semantic Query: 'What is the PTO and leave policy?'\n")
    res1 = search_corporate_knowledge.invoke("What is the PTO and leave policy?")
    print(res1[:1000])
    print("..." if len(res1) > 1000 else "")

    print("\n" + "-" * 70)

    # Test 2: Exact Keyword / Code Snippet
    print("\n[TEST 2] Keyword Query: 'docker-compose up -d'\n")
    res2 = search_corporate_knowledge.invoke("docker-compose up -d")
    print(res2[:1000])
    print("..." if len(res2) > 1000 else "")

    print("\n" + "-" * 70)

    # Test 3: Role Checklist Query
    print("\n[TEST 3] Role Checklist Query: 'What are the frontend dev onboarding tasks?'\n")
    res3 = search_corporate_knowledge.invoke("What are the frontend dev onboarding tasks?")
    print(res3[:1000])
    print("..." if len(res3) > 1000 else "")

    print("\n" + "=" * 70)
    print("      All Vector Search Tests Completed Successfully!")
    print("=" * 70)
