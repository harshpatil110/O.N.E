# ChromaDB Chunking & Embedding Rules

## Overview
The RAG pipeline in Nexus AI Innovations's O.N.E. platform uses **ChromaDB** as
the vector store for document embeddings. This document specifies the
chunking strategy.

## Chunking Strategy
* **Method:** Recursive Character Text Splitter (LangChain).
* **Chunk Size:** 1000 characters.
* **Chunk Overlap:** 200 characters.
* **Separators:** `["\n## ", "\n### ", "\n\n", "\n", " "]`

## Why These Settings?
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n## ", "\n### ", "\n\n", "\n", " "],
)
```
* **1000 chars** keeps chunks within the embedding model's sweet spot.
* **200 char overlap** prevents information loss at chunk boundaries.
* **Markdown-aware separators** ensure headers stay with their content.

## Embedding Model
* **Model:** `nomic-embed-text` via Ollama (768-dim vectors).
* **Batch Size:** 64 documents per batch.
* **Collection:** `one_knowledge_base`

## Metadata Attached to Each Chunk
```json
{
    "source": "03_architecture/system_overview.md",
    "chunk_index": 0,
    "total_chunks": 5,
    "category": "architecture",
    "created_at": "2026-08-01T00:00:00Z"
}
```

## Re-indexing Procedure
```bash
cd backend
python scripts/ingest_kb.py --force-rebuild
```
This drops the existing collection and re-indexes all files from
`knowledge_base/`.

---
*Data Engineering: Parth Shah*
