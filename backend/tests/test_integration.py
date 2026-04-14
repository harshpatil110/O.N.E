import pytest
import json
from unittest.mock import patch, MagicMock

@pytest.mark.asyncio
@patch("app.agents.orchestrator.RAGService.retrieve")
@patch("app.services.llm_service.AsyncOpenAI")
async def test_full_chat_pipeline(mock_openai_class, mock_retrieve):
    from httpx import AsyncClient, ASGITransport
    from app.main import app
    
    """
    Simulates a full end-to-end chat message pipeline:
    1. User hits POST /api/v1/chat/{session_id}/message
    2. Orchestrator evaluates state and queries RAG.
    3. RAG returns mocked context.
    4. Orchestrator constructs prompt and calls LLM.
    5. Mocked LLM returns response based on context.
    6. Orchestrator returns final message state.
    """
    
    # 1. Mock the Vector DB context returned by RAG
    mock_context_content = "We use Node.js version 20.x for all our applications."
    async def _mock_retrieve(*args, **kwargs):
        return [{
            "content": mock_context_content,
            "source": "fake_doc.md",
            "similarity_score": 0.99
        }]
    mock_retrieve.side_effect = _mock_retrieve
    
    # 2. Mock the OpenAI client
    mock_client = MagicMock()
    mock_openai_class.return_value = mock_client
    
    # Configure fake completion response choice
    mock_choice = MagicMock()
    mock_choice.message = MagicMock()
    mock_choice.message.content = "According to the docs, we use Node version 20.x."
    mock_choice.message.tool_calls = None
    mock_choice.message.model_dump.return_value = {
        "role": "assistant",
        "content": "According to the docs, we use Node version 20.x."
    }
    
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    
    async def mock_create(*args, **kwargs):
        return mock_response
        
    mock_client.chat.completions.create = MagicMock(side_effect=mock_create)
    
    # 3. Simulate the API Request
    session_id = "golden-test-session"
    payload = {"message": "what node version we use"}
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        response = await async_client.post(
            f"/api/v1/chat/{session_id}/message", 
            json=payload
        )
    
    # 4. Assertions
    # Status code check
    assert response.status_code == 200, f"Expected 200 OK but got {response.status_code}: {response.text}"
    
    # RAG was called once with the user's text
    assert mock_retrieve.call_count == 1
    assert mock_retrieve.call_args.kwargs.get("query") == "what node version we use"
    
    # LLM was called with the injected RAG context
    assert mock_client.chat.completions.create.called
    llm_call_kwargs = mock_client.chat.completions.create.call_args.kwargs
    messages = llm_call_kwargs.get("messages", [])
    
    # Search through all injected LLM messages to verify our fake DB content was fed into the LLM
    has_rag_context = False
    for msg in messages:
        if mock_context_content in str(msg.get("content", "")):
            has_rag_context = True
            break
            
    assert has_rag_context, "RAG context was not injected into the LLM messages."
    
    # Verify response JSON payload corresponds to ChatMessageResponse schema bounds
    data = response.json()
    assert "reply" in data
    assert "session_id" in data
    assert data["reply"] == "According to the docs, we use Node version 20.x."
