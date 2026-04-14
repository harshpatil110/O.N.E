import os
import json
import logging
import asyncio
import time
import re
from typing import List, Dict, Any, Optional

import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

from app.core.exceptions import LLMError, LLMRateLimitError, LLMParseError

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 4

class LLMService:
    def __init__(self):
        """
        Initializes the LLM service using Google Gemini.
        Configures the generative model with a default temperature and token limit.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.warning("GEMINI_API_KEY not found in environment.")
            
        genai.configure(api_key=api_key)
        self.model_name = "gemini-2.0-flash"
        self.generation_config = genai.types.GenerationConfig(
            temperature=0.3,
            max_output_tokens=2048
        )
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=self.generation_config
        )

    async def _call_with_retry(self, fn, *args, **kwargs):
        """
        Executes an LLM call with a retry strategy for rate limits.
        If all retries fail, returns a friendly error message.
        """
        for attempt in range(MAX_RETRIES):
            try:
                return await fn(*args, **kwargs)
            except (ResourceExhausted, Exception) as e:
                # Check if it's a rate limit error (429 or ResourceExhausted)
                error_msg = str(e).lower()
                is_rate_limit = isinstance(e, ResourceExhausted) or "429" in error_msg or "exhausted" in error_msg
                
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
        model = self.model
        if system_prompt:
            model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=self.generation_config,
                system_instruction=system_prompt
            )
            
        async def _generate():
            resp = await model.generate_content_async(prompt)
            if not resp.parts:
                return ""
            return resp.text
            
        return await self._call_with_retry(_generate)

    async def generate_with_tools(self, messages: List[Dict[str, Any]], tools: list, system_prompt: str) -> Dict[str, Any]:
        """
        Generates a response using defined tools, supporting multi-turn conversation history.

        Args:
            messages (List[Dict]): Conversation history in {'role': ..., 'content': ...} format.
            tools (list): List of tool definitions.
            system_prompt (str): Core behavioral instructions.

        Returns:
            Dict[str, Any]: A dictionary containing 'text' and a list of 'tool_calls'.
        """
        model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=self.generation_config,
            system_instruction=system_prompt,
            tools=tools
        )
        
        async def _generate():
            # Format messages based on Gemini expectations
            formatted_history = []
            for msg in messages:
                role = msg.get("role", "user")
                if role == "assistant":
                    role = "model"
                content = msg.get("content", "")
                
                # Omit empty content if needed
                formatted_history.append({"role": role, "parts": [content]})
                    
            resp = await model.generate_content_async(formatted_history)
            
            result = {
                "text": "",
                "tool_calls": []
            }
            
            if resp.parts:
                for part in resp.parts:
                    if hasattr(part, "text") and part.text:
                        result["text"] += part.text
                        
                    if hasattr(part, "function_call") and part.function_call:
                        # Map struct arguments to a simple dict
                        args_dict = type(part.function_call.args)(part.function_call.args) if type(part.function_call.args) is dict else dict(part.function_call.args)
                        
                        result["tool_calls"].append({
                            "name": part.function_call.name,
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
        
        # Override to json response mime type
        model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=genai.types.GenerationConfig(
                temperature=0.0,
                max_output_tokens=2048,
                response_mime_type="application/json"
            )
        )
        
        async def _generate():
            resp = await model.generate_content_async(full_prompt)
            if not resp.parts:
                 return "{}"
            return resp.text
            
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
