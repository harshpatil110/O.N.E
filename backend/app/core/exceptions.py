class LLMError(Exception):
    """Base exception for LLM service errors."""
    pass

class LLMRateLimitError(LLMError):
    """Exception raised when the LLM service rate limit is exceeded."""
    pass

class LLMParseError(LLMError):
    """Exception raised when failing to parse the structured output from the LLM."""
    pass

class InvalidTransitionError(Exception):
    """Exception raised for invalid FSM state transitions."""
    pass
