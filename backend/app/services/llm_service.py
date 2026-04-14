import os
import json
import logging
import asyncio
import time
import re
from typing import List, Dict, Any, Optional

from openai import AsyncOpenAI
import openai

from app.core.exceptions import LLMError, LLMRateLimitError, LLMParseError
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

# 1. FORCE the environment variables to load immediately
load_dotenv()

class LLMService:
    def __init__(self):
        # 2. Grab the key and explicitly check if it exists
        api_key = os.getenv("NVIDIA_API_KEY") 
        
        if not api_key:
            print("🚨 URGENT: NVIDIA_API_KEY is missing or empty!")
            
        self.client = AsyncOpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=api_key
        )
logger = logging.getLogger(__name__)

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 4

class LLMService:
    def __init__(self):
        """
        Initializes the LLM service using OpenAI SDK for Nvidia NIM.
        """
        api_key = os.getenv("NVIDIA_API_KEY")
        if not api_key:
            logger.warning("NVIDIA_API_KEY not found in environment.")
            
        self.client = AsyncOpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=api_key or "dummy-key"
        )
        self.model_name = os.getenv("NVIDIA_MODEL_NAME", "meta/llama3-70b-instruct")

    async def _call_with_retry(self, fn, *args, **kwargs):
        """
        Executes an LLM call with a retry strategy for rate limits.
        If all retries fail, returns a friendly error message.
        """
        for attempt in range(MAX_RETRIES):
            try:
                return await fn(*args, **kwargs)
            except Exception as e:
                # Check if it's a rate limit error
                error_msg = str(e).lower()
                is_rate_limit = "429" in error_msg or "rate limit" in error_msg or "exhausted" in error_msg
                
                if is_rate_limit:
                    logger.warning(f"Rate limit hit. Attempt {attempt + 1}/{MAX_RETRIES} failed.")
                    if attempt < MAX_RETRIES - 1:
                        # Short blocking delay as requested
                        time.sleep(2)
                        continue
                    return "I'm receiving too many messages right now. Please wait a moment and try again!"
                
                # For generic exceptions, log and return fallback
                logger.error(f"Unexpected LLM API error: {str(e)}")
                return "I encountered an unexpected error while processing your request. Please try again shortly."

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generates a direct text response for a given prompt.

        Args:
            prompt (str): The user input or specific instruction.
            system_prompt (str, optional): Overriding system instructions.

        Returns:
            str: The generated text content.
        """
        async def _generate():
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            resp = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.3,
                max_tokens=2048
            )
            return resp.choices[0].message.content or ""
            
        return await self._call_with_retry(_generate)

    async def generate_with_tools(self, messages: List[Dict[str, Any]], tools: list, system_prompt: str) -> Dict[str, Any]:
        """
        Generates a response using defined tools, supporting multi-turn conversation history.

        Args:
            messages (List[Dict]): Conversation history in {'role': ..., 'content': ...} format.
            tools (list): List of tool definitions.
            system_prompt (str): Core behavioral instructions.

        Returns:
            Dict[str, Any]: A dictionary containing 'text', 'tool_calls', and 'raw_message'.
        """
        async def _generate():
            formatted_history = []
            if system_prompt:
                formatted_history.append({"role": "system", "content": system_prompt})
                
            for msg in messages:
                role = msg.get("role", "user")
                if role == "model":
                    role = "assistant"
                    
                formatted_msg = {"role": role}
                if msg.get("content"):
                    formatted_msg["content"] = msg["content"]
                
                if role == "tool":
                    formatted_msg["tool_call_id"] = msg.get("tool_call_id", "unknown")
                    # Content must be a string containing the result
                    formatted_msg["content"] = msg.get("content", "{}")
                    
                formatted_history.append(formatted_msg)
                
            resp = await self.client.chat.completions.create(
                model=self.model_name,
                messages=formatted_history,
                tools=tools,
                temperature=0.3,
                max_tokens=2048
            )
            
            result = {
                "text": "",
                "tool_calls": []
            }
            
            message = resp.choices[0].message
            if message.content:
                result["text"] = message.content
            
            # Pass the raw message back so it can be appended to history
            result["raw_message"] = message.model_dump(exclude_unset=True)
                
            if message.tool_calls:
                for tc in message.tool_calls:
                    # Map struct arguments to a simple dict
                    try:
                        args_dict = json.loads(tc.function.arguments)
                    except json.JSONDecodeError:
                        args_dict = {}
                        
                    result["tool_calls"].append({
                        "id": tc.id,
                        "name": tc.function.name,
                        "args": args_dict
                    })
                        
            return result
            
        result = await self._call_with_retry(_generate)
        if isinstance(result, str):
            return {"text": result, "tool_calls": []}
        return result

    async def extract_structured(self, prompt: str, output_schema: dict) -> dict:
        """
        Uses constrained generation to extract structured data matching a JSON schema.

        Args:
            prompt (str): The raw text to process.
            output_schema (dict): The target JSON schema.

        Returns:
            dict: The extracted data.

        Raises:
            LLMParseError: If the output cannot be parsed as valid JSON.
        """
        instruction = "Respond ONLY with valid JSON exactly matching the following schema:\n"
        instruction += json.dumps(output_schema, indent=2)
        instruction += "\nDo not include code blocks or markdown, just the raw JSON object."
        
        full_prompt = f"{instruction}\n\nInput to process:\n{prompt}"
        
        async def _generate():
            # Nvidia NIM supports JSON output format if supported by the model
            # We'll use standard generation with a strong prompt
            resp = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": full_prompt}],
                temperature=0.0,
                max_tokens=2048,
                response_format={"type": "json_object"}
            )
            return resp.choices[0].message.content or "{}"
            
        text_resp = await self._call_with_retry(_generate)
        
        # If _call_with_retry returned the error string, we can't parse it as JSON
        if "too many messages" in text_resp or "unexpected error" in text_resp:
            logger.error(f"Structured extraction failed due to LLM error: {text_resp}")
            return {}

        try:
            # Strip markdown block if model ignored the instruction
            cleaned_text = re.sub(r'^```json\s*', '', text_resp.strip())
            cleaned_text = re.sub(r'^```\s*', '', cleaned_text)
            cleaned_text = re.sub(r'\s*```$', '', cleaned_text)
            
            return json.loads(cleaned_text.strip())
        except json.JSONDecodeError as e:
            raise LLMParseError(f"Failed to parse LLM structured output as JSON: {e}. Output was: {text_resp}")
