#!/usr/bin/env python3
"""
ingest_kb.py — Knowledge Base Vectorization & ChromaDB Ingestion
=================================================================
Loads all Markdown files from backend/knowledge_base/, chunks them with
RecursiveCharacterTextSplitter, embeds with a local HuggingFace model,
and persists to a ChromaDB vector store at backend/chroma_db/.

Usage:
    pip install langchain langchain-chroma langchain-huggingface sentence-transformers chromadb
    python scripts/ingest_kb.py
"""

import os
import sys
import shutil
import time

# ─── Resolve paths relative to this script ────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(SCRIPT_DIR, "..")
KB_DIR = os.path.join(BACKEND_DIR, "knowledge_base")
CHROMA_DIR = os.path.join(BACKEND_DIR, "chroma_db")
COLLECTION_NAME = "one_knowledge_base"

# ─── Configuration ────────────────────────────────────────────────────────────
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def main():
    start_time = time.time()

    print("=" * 65)
    print("  O.N.E. Knowledge Base Ingestion Pipeline")
    print("=" * 65)
    print(f"  Input:      {os.path.abspath(KB_DIR)}")
    print(f"  Output:     {os.path.abspath(CHROMA_DIR)}")
    print(f"  Collection: {COLLECTION_NAME}")
    print(f"  Chunk size: {CHUNK_SIZE}  |  Overlap: {CHUNK_OVERLAP}")
    print(f"  Embedding:  {EMBEDDING_MODEL}")
    print("=" * 65)

    # ── Validate input directory ──────────────────────────────────────────
    if not os.path.isdir(KB_DIR):
        print(f"\n[ERROR] Knowledge base directory not found: {KB_DIR}")
        print("        Run generate_kb.py first.")
        sys.exit(1)

    # ── Step 1: Idempotency — clear existing vector store ─────────────────
    if os.path.exists(CHROMA_DIR):
        print("\n[1/5] Clearing existing ChromaDB store for clean re-ingestion...")
        shutil.rmtree(CHROMA_DIR)
        print("       Old chroma_db/ removed.")
    else:
        print("\n[1/5] No existing ChromaDB store found. Starting fresh.")

    # ── Step 2: Load documents ────────────────────────────────────────────
    print("\n[2/5] Loading Markdown documents...")

    from langchain_community.document_loaders import DirectoryLoader, TextLoader

    loader = DirectoryLoader(
        KB_DIR,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
        use_multithreading=True,
    )
    documents = loader.load()
    doc_count = len(documents)

    if doc_count == 0:
        print("[ERROR] No documents loaded. Check the knowledge_base/ directory.")
        sys.exit(1)

    print(f"       Loaded {doc_count} documents.")

    # ── Step 3: Chunk documents ───────────────────────────────────────────
    print(f"\n[3/5] Splitting documents (chunk_size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})...")

    from langchain_text_splitters import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n#### ", "\n\n", "\n", " ", ""],
        length_function=len,
    )
    chunks = splitter.split_documents(documents)
    chunk_count = len(chunks)
    print(f"       Created {chunk_count} chunks from {doc_count} documents.")
    print(f"       Average chunks per document: {chunk_count / doc_count:.1f}")

    # Enrich metadata with category and chunk index
    for i, chunk in enumerate(chunks):
        source = chunk.metadata.get("source", "")
        # Extract category folder from path (e.g. "01_hr_and_culture")
        rel_path = os.path.relpath(source, KB_DIR) if source else ""
        parts = rel_path.replace("\\", "/").split("/")
        chunk.metadata["category"] = parts[0] if len(parts) > 1 else "uncategorized"
        chunk.metadata["chunk_index"] = i
        chunk.metadata["total_chunks"] = chunk_count

    # ── Step 4: Initialize embeddings ─────────────────────────────────────
    print(f"\n[4/5] Loading embedding model: {EMBEDDING_MODEL}")
    print("       (First run will download ~80MB model — subsequent runs use cache)")

    from langchain_huggingface import HuggingFaceEmbeddings

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    print("       Embedding model loaded successfully.")

    # ── Step 5: Create ChromaDB vector store ──────────────────────────────
    print(f"\n[5/5] Persisting {chunk_count} chunks to ChromaDB...")

    from langchain_chroma import Chroma

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=os.path.abspath(CHROMA_DIR),
    )

    # Verify the store
    stored_count = vectorstore._collection.count()
    elapsed = time.time() - start_time

    # ── Summary ───────────────────────────────────────────────────────────
    print("\n" + "=" * 65)
    print("  INGESTION COMPLETE")
    print("=" * 65)
    print(f"  Documents loaded:    {doc_count}")
    print(f"  Chunks created:      {chunk_count}")
    print(f"  Vectors stored:      {stored_count}")
    print(f"  Collection name:     {COLLECTION_NAME}")
    print(f"  Persist directory:   {os.path.abspath(CHROMA_DIR)}")
    print(f"  Embedding model:     {EMBEDDING_MODEL}")
    print(f"  Time elapsed:        {elapsed:.1f}s")
    print("=" * 65)

    # ── Quick sanity test ─────────────────────────────────────────────────
    print("\n  Running sanity search: 'How do I set up my VPN?'")
    results = vectorstore.similarity_search("How do I set up my VPN?", k=3)
    for i, doc in enumerate(results, 1):
        source = os.path.basename(doc.metadata.get("source", "unknown"))
        preview = doc.page_content[:120].replace("\n", " ").strip()
        print(f"    [{i}] {source}: {preview}...")

    print("\n  The knowledge base is ready for RAG queries!")
    print("=" * 65)


if __name__ == "__main__":
    main()
