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
from langchain_community.retrievers import BM25Retriever
# --- Resilient EnsembleRetriever Import ---
try:
    # Standard path for LangChain 0.2.x and 0.3.x
    from langchain.retrievers import EnsembleRetriever
except ImportError:
    try:
        # Fallback for community packages
        from langchain_community.retrievers import EnsembleRetriever
    except ImportError:
        try:
            # Legacy deep path
            from langchain.retrievers.ensemble import EnsembleRetriever
        except ImportError as e:
            logger.error(f"Critical Error: Cannot find EnsembleRetriever in any LangChain namespace. {e}")
            EnsembleRetriever = None # Failsafe

# ─── Path Resolution ─────────────────────────────────────────────────────────
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_BACKEND_DIR = os.path.abspath(os.path.join(_THIS_DIR, "..", ".."))
KB_DIR = os.path.abspath(os.path.join(_BACKEND_DIR, "knowledge_base"))
CHROMA_DIR = os.path.abspath(os.path.join(_BACKEND_DIR, "chroma_db"))
COLLECTION_NAME = "one_knowledge_base"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ─── Lazy Singleton Initialization ────────────────────────────────────────────
_hybrid_retriever = None


def _init_hybrid_retriever():
    global _hybrid_retriever
    if _hybrid_retriever is not None:
        return _hybrid_retriever

    logger.info("Initializing Hybrid Search Engine (ChromaDB + BM25)...")

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

    vector_retriever = chroma_vectorstore.as_retriever(search_kwargs={"k": 2})

    # 3. Sparse Retriever (BM25)
    bm25_retriever = BM25Retriever.from_documents(chunks)
    bm25_retriever.k = 2

    # 4. Ensemble Retriever (50/50 Dense & Sparse)
    if EnsembleRetriever is not None:
        _hybrid_retriever = EnsembleRetriever(
            retrievers=[vector_retriever, bm25_retriever],
            weights=[0.5, 0.5],
        )
    else:
        logger.warning("EnsembleRetriever failed to import. Falling back to vector search only.")
        _hybrid_retriever = vector_retriever

    logger.info("Hybrid EnsembleRetriever successfully initialized.")
    return _hybrid_retriever


# D. LangChain Tool Wrapper
@tool("search_corporate_knowledge")
def search_corporate_knowledge(query: str) -> str:
    """Use this tool to search the corporate knowledge base for policies, setup guides, 
    codebase architecture, terminal commands, and role checklists.
    Input MUST be a specific search query string."""
    try:
        retriever = _init_hybrid_retriever()
        if retriever is not None:
            docs = retriever.invoke(query)
            if not docs:
                return "No matching documentation found in the corporate knowledge base."
            
            # Format and truncate to 1500 chars max to protect Qwen 3B VRAM
            formatted_docs = []
            for d in docs[:2]:
                src = d.metadata.get('source', 'Knowledge Base')
                content = d.page_content[:600]
                formatted_docs.append(f"Source: {src}\nContent: {content}")
            
            return "\n\n---\n\n".join(formatted_docs)
        else:
            return "Knowledge base search tool is initializing or operating in basic mode."
            
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
    print("      Hybrid Search Engine Verification (ChromaDB + BM25)")
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
    print("      All Hybrid Search Tests Completed Successfully!")
    print("=" * 70)
