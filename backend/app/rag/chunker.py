from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Dict, Any

def chunk_documents(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Split each document into chunks of ~512 tokens with 50-token overlap.
    Preserve metadata from parent document in each chunk.
    Each chunk gets a unique ID: "{source}:chunk_{n}"
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,     # ~512 tokens at ~4 chars/token
        chunk_overlap=200,   # ~50 tokens overlap
        separators=["\n## ", "\n### ", "\n\n", "\n", " "]
        # Split on headings first to preserve section coherence
    )
    chunks = []
    for doc in documents:
        texts = splitter.split_text(doc["content"])
        for i, text in enumerate(texts):
            # Create a new metadata dict for each chunk containing the parent's metadata and its chunk_index
            metadata = {**doc["metadata"], "chunk_index": i}
            chunks.append({
                "id": f"{doc['metadata']['source']}:chunk_{i}",
                "content": text,
                "metadata": metadata
            })
    return chunks
