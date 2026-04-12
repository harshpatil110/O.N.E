import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock

from google.api_core.exceptions import ResourceExhausted

from app.services.llm_service import LLMService, MAX_RETRIES
from app.core.exceptions import LLMRateLimitError, LLMParseError

@pytest.fixture
def llm_service():
    with patch("google.generativeai.configure"), patch("google.generativeai.GenerativeModel"):
        service = LLMService()
        return service

@pytest.mark.asyncio
async def test_generate_success(llm_service):
    mock_response = MagicMock()
    mock_response.parts = [MagicMock(text="Hello, World!")]
    mock_response.text = "Hello, World!"
    
    with patch.object(llm_service.model, "generate_content_async", new_callable=AsyncMock) as mock_generate:
        mock_generate.return_value = mock_response
        
        result = await llm_service.generate("Say hello")
        
        assert result == "Hello, World!"
        mock_generate.assert_called_once_with("Say hello")

@pytest.mark.asyncio
async def test_retry_logic_on_rate_limit(llm_service):
    with patch.object(llm_service.model, "generate_content_async", new_callable=AsyncMock) as mock_generate, \
         patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
             
        # Make the mock raise ResourceExhausted every time
        mock_generate.side_effect = ResourceExhausted("Rate limit exceeded")
        
        with pytest.raises(LLMRateLimitError):
            await llm_service.generate("Trigger rate limit")
            
        assert mock_generate.call_count == MAX_RETRIES
        assert mock_sleep.call_count == MAX_RETRIES - 1

@pytest.mark.asyncio
async def test_extract_structured_success(llm_service):
    mock_response = MagicMock()
    mock_response.parts = [MagicMock()]
    mock_response.text = '```json\n{"name": "Jane", "role": "frontend"}\n```'
    
    with patch("google.generativeai.GenerativeModel") as MockModel:
        # We need to mock instance returned by MockModel
        mock_instance = MockModel.return_value
        mock_instance.generate_content_async = AsyncMock(return_value=mock_response)
        
        schema = {"name": "string", "role": "string"}
        
        result = await llm_service.extract_structured("My name is Jane and I am frontend", schema)
        
        assert isinstance(result, dict)
        assert result["name"] == "Jane"
        assert result["role"] == "frontend"
        
        # Verify the prompt contained our instructions
        call_args = mock_instance.generate_content_async.call_args[0][0]
        assert "Respond ONLY with valid JSON" in call_args

@pytest.mark.asyncio
async def test_extract_structured_parse_error(llm_service):
    mock_response = MagicMock()
    mock_response.parts = [MagicMock()]
    # Invalid JSON string
    mock_response.text = "Not JSON format at all"
    
    with patch("google.generativeai.GenerativeModel") as MockModel:
        mock_instance = MockModel.return_value
        mock_instance.generate_content_async = AsyncMock(return_value=mock_response)
        
        schema = {"name": "string"}
        
        with pytest.raises(LLMParseError):
            await llm_service.extract_structured("Bad output", schema)
