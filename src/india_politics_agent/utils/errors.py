"""Custom exception hierarchy for the agent."""


class AgentError(Exception):
    """Base exception for all agent errors."""

    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class ConfigurationError(AgentError):
    """Configuration-related errors."""
    pass


class APIError(AgentError):
    """API-related errors."""

    def __init__(self, message: str, api_name: str = None, status_code: int = None, **kwargs):
        super().__init__(message, kwargs)
        self.api_name = api_name
        self.status_code = status_code


class RateLimitError(APIError):
    """Rate limit exceeded errors."""
    pass


class QuotaExhaustedError(APIError):
    """API quota exhausted errors."""
    pass


class WebScrapingError(AgentError):
    """Web scraping related errors."""

    def __init__(self, message: str, url: str = None, **kwargs):
        super().__init__(message, kwargs)
        self.url = url


class CacheError(AgentError):
    """Cache-related errors."""
    pass


class ValidationError(AgentError):
    """Input validation errors."""

    def __init__(self, message: str, field: str = None, value=None, **kwargs):
        super().__init__(message, kwargs)
        self.field = field
        self.value = value


class AnalysisError(AgentError):
    """Analysis generation errors."""

    def __init__(self, message: str, topic: str = None, stage: str = None, **kwargs):
        super().__init__(message, kwargs)
        self.topic = topic
        self.stage = stage


class TimeoutError(AgentError):
    """Operation timeout errors."""

    def __init__(self, message: str, operation: str = None, timeout_seconds: float = None, **kwargs):
        super().__init__(message, kwargs)
        self.operation = operation
        self.timeout_seconds = timeout_seconds
