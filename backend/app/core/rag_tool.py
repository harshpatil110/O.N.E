#!/usr/bin/env python3
"""
rag_tool.py — Hybrid Search Engine & Agentic RAG Tool
======================================================
Combines ChromaDB dense vector search with BM25 sparse keyword search
via an EnsembleRetriever, and exposes the hybrid engine as a LangChain
@tool for the Hermes Supervisor Agent.

Components:
    - ChromaDB (dense):  sentence-transformers/all-MiniLM-L6-v2
    - BM25 (sparse):     rank_bm25 in-memory keyword index
    - EnsembleRetriever: 50/50 weighted merge of both retrievers
"""

import os
import logging

from langchain_core.tools import tool

logger = logging.getLogger(__name__)

# ─── Path Resolution ─────────────────────────────────────────────────────────
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_BACKEND_DIR = os.path.join(_THIS_DIR, "..", "..")
KB_DIR = os.path.abspath(os.path.join(_BACKEND_DIR, "knowledge_base"))
CHROMA_DIR = os.path.abspath(os.path.join(_BACKEND_DIR, "chroma_db"))
COLLECTION_NAME = "one_knowledge_base"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ─── Lazy singletons (initialized on first call) ─────────────────────────────
_hybrid_retriever = None


def _load_kb_documents():
    """Load all markdown files from the knowledge_base/ directory."""
    from langchain_community.document_loaders import DirectoryLoader, TextLoader

    loader = DirectoryLoader(
        KB_DIR,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        use_multithreading=True,
    )
    docs = loader.load()
    logger.info("BM25: Loaded %d documents from %s", len(docs), KB_DIR)
    return docs


def _build_hybrid_retriever():
    """
    Build and return an EnsembleRetriever combining:
      - ChromaDB vector retriever (dense / semantic)
      - BM25Retriever (sparse / keyword)
    Both contribute equally (50/50 weight).
    """
    global _hybrid_retriever
    if _hybrid_retriever is not None:
        return _hybrid_retriever

    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_chroma import Chroma
    from langchain_community.retrievers import BM25Retriever
    from langchain_classic.retrievers import EnsembleRetriever
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    logger.info("Initializing Hybrid Search Engine...")

    # ── 1. Dense Retriever (ChromaDB) ─────────────────────────────────────
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings,
    )

    vector_retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3},
    )
    logger.info("Dense retriever ready (ChromaDB: %s)", CHROMA_DIR)

    # ── 2. Sparse Retriever (BM25) ───────────────────────────────────────
    raw_docs = _load_kb_documents()

    # Chunk the raw docs with the same splitter used during ingestion so
    # BM25 operates on comparable text units.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=["\n## ", "\n### ", "\n#### ", "\n\n", "\n", " ", ""],
    )
    chunked_docs = splitter.split_documents(raw_docs)

    bm25_retriever = BM25Retriever.from_documents(chunked_docs)
    bm25_retriever.k = 3
    logger.info("Sparse retriever ready (BM25: %d chunks indexed)", len(chunked_docs))

    # ── 3. Ensemble (Hybrid) ─────────────────────────────────────────────
    _hybrid_retriever = EnsembleRetriever(
        retrievers=[vector_retriever, bm25_retriever],
        weights=[0.5, 0.5],
    )
    logger.info("Hybrid EnsembleRetriever initialized (50/50 dense/sparse)")

    return _hybrid_retriever


def _format_results(docs) -> str:
    """
    Convert a list of LangChain Document objects into a single readable
    string suitable for consumption by an LLM agent.
    """
    if not docs:
        return "No relevant documents found in the knowledge base."

    parts = []
    for i, doc in enumerate(docs, 1):
        source = os.path.basename(doc.metadata.get("source", "unknown"))
        parts.append(
            f"--- Source [{i}]: {source} ---\n{doc.page_content.strip()}"
        )
    return "\n\n".join(parts)


# ═════════════════════════════════════════════════════════════════════════════
# THE AGENTIC TOOL
# ═════════════════════════════════════════════════════════════════════════════

@tool
def search_company_knowledge_base(query: str) -> str:
    """Use this tool to search the Nexus AI Innovations corporate knowledge
    base. It performs a hybrid search combining semantic understanding with
    exact keyword matching for maximum recall.

    Use this tool when the user asks about:
    - HR policies (PTO, remote work, benefits, performance reviews, ethics)
    - Onboarding procedures (Day 1 checklist, VPN setup, SSH keys, Jira access)
    - System architecture (FastAPI backend, React frontend, Hermes Agent,
      ChromaDB, multi-agent design)
    - Coding standards (PEP 8, React best practices, Git branching, Alembic
      migrations, API conventions)
    - DevOps (Docker-compose, CI/CD pipelines, environment variables,
      monitoring)
    - Team directory (contact info for Harshvardhan Patil, Parth Shah,
      Manas Gupta, Archit Verma)
    - API specifications (endpoint details, request/response schemas)
    - MCP tool specifications (Jira and GitHub Model Context Protocol tools)

    Input should be a specific, detailed search query describing exactly
    what information you need. For example:
    - "What is the PTO leave policy and how many vacation days per year?"
    - "How do I set up WireGuard VPN for remote access?"
    - "What is the Git branching strategy and PR checklist?"

    Returns relevant excerpts from the knowledge base with source file
    references.
    """
    retriever = _build_hybrid_retriever()
    results = retriever.invoke(query)
    return _format_results(results)


# ═════════════════════════════════════════════════════════════════════════════
# LOCAL TEST BLOCK
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    )

    print("=" * 65)
    print("  Hybrid RAG Tool — Local Test")
    print("=" * 65)

    # Test 1: Semantic / conceptual query
    print("\n[TEST 1] Semantic query: 'What is the PTO policy?'\n")
    result1 = search_company_knowledge_base.invoke("What is the PTO policy?")
    print(result1[:800])
    print("..." if len(result1) > 800 else "")

    print("\n" + "-" * 65)

    # Test 2: Exact keyword query (code snippet / command)
    print("\n[TEST 2] Keyword query: 'docker-compose up -d'\n")
    result2 = search_company_knowledge_base.invoke("docker-compose up -d")
    print(result2[:800])
    print("..." if len(result2) > 800 else "")

    print("\n" + "-" * 65)

    # Test 3: Team directory query
    print("\n[TEST 3] Entity query: 'Harshvardhan Patil contact information'\n")
    result3 = search_company_knowledge_base.invoke(
        "Harshvardhan Patil contact information"
    )
    print(result3[:800])
    print("..." if len(result3) > 800 else "")

    print("\n" + "=" * 65)
    print("  All tests complete.")
    print("=" * 65)
