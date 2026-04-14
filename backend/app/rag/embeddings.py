import os
import openai

class NvidiaEmbeddingFunction:
    """ChromaDB-compatible embedding function using Nvidia NV-EmbedQA."""

    def __init__(self):
        api_key = os.getenv("NVIDIA_API_KEY")
        self.client = openai.OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=api_key or "dummy-key"
        )
        self.model_name = "nvidia/nv-embedqa-e5-v5"

    def __call__(self, input: list[str]) -> list[list[float]]:
        embeddings = []
        # Process in batches if necessary, though ingest handles small batches natively
        batch_size = 50
        for i in range(0, len(input), batch_size):
            batch = input[i:i + batch_size]
            response = self.client.embeddings.create(
                input=batch,
                model=self.model_name,
                extra_body={"input_type": "passage", "truncate": "END"}
            )
            for data in response.data:
                embeddings.append(data.embedding)
        return embeddings

def embed_query(text: str) -> list[float]:
    """Embed a query string using NV-EmbedQA."""
    client = openai.OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=os.getenv("NVIDIA_API_KEY") or "dummy-key"
    )
    response = client.embeddings.create(
        input=[text],
        model="nvidia/nv-embedqa-e5-v5",
        extra_body={"input_type": "query", "truncate": "END"}
    )
    return response.data[0].embedding
