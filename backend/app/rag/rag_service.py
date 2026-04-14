import logging
from typing import List, Dict, Any, Optional
from app.rag.chroma_client import get_collection
from app.rag.embeddings import embed_query

logger = logging.getLogger(__name__)

class RAGService:
    """
    Handles similarity search and retrieval of documentation chunks from ChromaDB.
    """
    def __init__(self):
        """Initializes the service and connects to the ChromaDB collection."""
        self.collection = get_collection()

    async def retrieve(
        self,
        query: str,
        role: Optional[str] = None,
        tech_stack: Optional[list] = None,
        checklist_item=None,
        category: Optional[str] = None,
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Retrieves relevant documentation chunks using semantic search.

        Args:
            query (str): The search query (usually a user question or task description).
            role (str, optional): The user's role to filter by.
            tech_stack (list, optional): The user's tech stack to filter by.
            category (str, optional): The document category (e.g., 'security', 'onboarding').
            top_k (int): Number of documents to return.

        Returns:
            List[Dict]: A list of retrieved documents with content and similarity scores.
        """
        
        # 1. Build where clause for ChromaDB metadata filter
        where_conditions = []
        if role:
            where_conditions.append({"applicable_roles": {"$contains": role}})
        if category:
            where_conditions.append({"category": {"$eq": category}})
        
        where = {"$and": where_conditions} if len(where_conditions) > 1 \
                else where_conditions[0] if where_conditions else None
        
        # 2. Embed the query
        query_embedding = embed_query(query)
        
        # Handle empty collection gracefully
        collection_count = self.collection.count()
        if collection_count == 0:
            return []

        # 3. Semantic search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(10, collection_count),
            where=where,
            include=["documents", "metadatas", "distances"]
        )
        
        # 4. Format results
        documents = []
        if results.get("documents") and results["documents"][0]:
            docs = results["documents"][0]
            metas = results["metadatas"][0] if results.get("metadatas") else [{}] * len(docs)
            dists = results["distances"][0] if results.get("distances") else [0.0] * len(docs)
            
            for doc, meta, dist in zip(docs, metas, dists):
                if doc is None or meta is None:
                    continue
                documents.append({
                    "content": doc,
                    "source": meta.get("source", "unknown"),
                    "title": meta.get("title", ""),
                    "category": meta.get("category", ""),
                    "similarity_score": 1.0 - dist  # convert distance to similarity
                })
        
        # 5. Filter by confidence threshold — don't include very low-relevance docs
        documents = [d for d in documents if d["similarity_score"] >= 0.4]
        
        # Sort descending by similarity
        documents.sort(key=lambda x: x["similarity_score"], reverse=True)
        
        # 6. Return top_k results
        return documents[:top_k]

    def format_for_prompt(self, documents: List[Dict[str, Any]]) -> str:
        """
        Formats retrieved documents into a string for injection into an LLM prompt.

        Args:
            documents (List[Dict]): The list of document dictionaries from retrieve().

        Returns:
            str: The formatted context string.
        """
        if not documents:
            return ""
        
        formatted = "\n\n--- RETRIEVED DOCUMENTATION ---\n"
        for doc in documents:
            formatted += f"\n[Source: {doc['source']}]\n{doc['content']}\n"
        formatted += "\n--- END OF DOCUMENTATION ---\n"
        return formatted
