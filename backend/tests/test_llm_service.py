import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock

from app.services.llm_service import LLMService, MAX_RETRIES
from app.core.exceptions import LLMParseError

@pytest.fixture
def mock_openai_client():
    with patch("app.services.llm_service.AsyncOpenAI") as mock_openai:
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        yield mock_client

@pytest.fixture
def llm_service(mock_openai_client):
    service = LLMService()
    return service

@pytest.mark.asyncio
async def test_generate_success(llm_service, mock_openai_client):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Hello, World!"
    
    mock_openai_client.chat.completions.create = AsyncMock(return_value=mock_response)
    
    result = await llm_service.generate("Say hello")
    
    assert result == "Hello, World!"
    mock_openai_client.chat.completions.create.assert_called_once()
    kwargs = mock_openai_client.chat.completions.create.call_args.kwargs
    assert kwargs["messages"][0]["content"] == "Say hello"

@pytest.mark.asyncio
async def test_retry_logic_on_rate_limit(llm_service, mock_openai_client):
    with patch("time.sleep") as mock_sleep:
        # Make the mock raise a rate limit error (Exception with 429 in it)
        mock_openai_client.chat.completions.create = AsyncMock(side_effect=Exception("Rate limit 429 exceeded"))
        
        result = await llm_service.generate("Trigger rate limit")
        
        # In current implementation, it doesn't raise, it returns a fallback string
        assert "too many messages" in result.lower()
        assert mock_openai_client.chat.completions.create.call_count == MAX_RETRIES
        assert mock_sleep.call_count == MAX_RETRIES - 1

@pytest.mark.asyncio
async def test_extract_structured_success(llm_service, mock_openai_client):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = '```json\n{"name": "Jane", "role": "frontend"}\n```'
    
    mock_openai_client.chat.completions.create = AsyncMock(return_value=mock_response)
    
    schema = {"name": "string", "role": "string"}
    
    result = await llm_service.extract_structured("My name is Jane and I am frontend", schema)
    
    assert isinstance(result, dict)
    assert result["name"] == "Jane"
    assert result["role"] == "frontend"
    
    # Verify the prompt contained our instructions
    kwargs = mock_openai_client.chat.completions.create.call_args.kwargs
    call_content = kwargs["messages"][0]["content"]
    assert "Respond ONLY with valid JSON" in call_content

@pytest.mark.asyncio
async def test_extract_structured_parse_error(llm_service, mock_openai_client):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Not JSON format at all"
    
    mock_openai_client.chat.completions.create = AsyncMock(return_value=mock_response)
    
    schema = {"name": "string"}
    
    with pytest.raises(LLMParseError):
        await llm_service.extract_structured("Bad output", schema)
