import pytest
from app.rag.rag_service import RAGService

test_queries = [
    {
        "query": "How do I install Python 3.11?",
        "expected_source_contains": "local-dev-python",
        "role": "backend"
    },
    {
        "query": "What is the branch naming convention?",
        "expected_source_contains": "git-workflow",
        "role": "backend"
    },
    {
        "query": "What does the NDA cover?",
        "expected_source_contains": "nda-ip-agreement",
        "role": "backend"
    },
    {
        "query": "How do I run the project with Docker?",
        "expected_source_contains": "docker-setup",
        "role": "devops"
    },
    {
        "query": "What are the code review requirements?",
        "expected_source_contains": "code-review-process",
        "role": "backend"
    }
]

@pytest.mark.asyncio
async def test_rag_retrieval_service():
    """
    Given an ingested knowledge base, tests that the semantic search and 
    metadata filtering logic retrieves the expected document sources.
    """
    rag = RAGService()
    
    for case in test_queries:
        results = await rag.retrieve(
            query=case["query"],
            role=case["role"],
            top_k=3
        )
        
        # Verify that we got at least one result
        assert len(results) > 0, f"No results found for query: {case['query']}"
        
        # Verify the expected source is among the retrieved documents
        sources = [doc["source"] for doc in results]
        
        found_expected = any(case["expected_source_contains"] in src for src in sources)
        assert found_expected, (
            f"Expected source containing '{case['expected_source_contains']}' "
            f"not found in top results. Found: {sources}"
        )
