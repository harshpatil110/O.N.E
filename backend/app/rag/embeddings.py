import os
import google.generativeai as genai

class GeminiEmbeddingFunction:
    """ChromaDB-compatible embedding function using Gemini text-embedding-004."""

    def __init__(self):
        # API Key should be set with genai.configure before calling this or inside here
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
        self.model_name = "models/text-embedding-004"

    def __call__(self, input: list[str]) -> list[list[float]]:
        embeddings = []
        for text in input:
            result = genai.embed_content(
                model=self.model_name,
                content=text,
                task_type="retrieval_document"
            )
            embeddings.append(result["embedding"])
        return embeddings

def embed_query(text: str) -> list[float]:
    """Embed a query string using RETRIEVAL_QUERY task type."""
    # API Key should be set with genai.configure before calling this or inside here
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type="retrieval_query"  # Different task type for queries vs documents
    )
    return result["embedding"]
