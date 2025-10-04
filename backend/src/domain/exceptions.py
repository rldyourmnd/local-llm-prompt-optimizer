"""Domain exceptions for prompt optimization."""


class DomainException(Exception):
    """Base domain exception."""
    code: str = "DOMAIN_ERROR"
    message: str = "Domain error occurred"

    def __init__(self, message: str = None):
        self.message = message or self.message
        super().__init__(self.message)


class VendorNotSupportedException(DomainException):
    """Vendor not supported."""
    code = "VENDOR_NOT_SUPPORTED"
    message = "Requested vendor is not supported"


class LLMClientException(DomainException):
    """LLM client error."""
    code = "LLM_CLIENT_ERROR"
    message = "LLM client operation failed"


class OptimizationFailedException(DomainException):
    """Optimization failed."""
    code = "OPTIMIZATION_FAILED"
    message = "Prompt optimization failed"


class InvalidPromptException(DomainException):
    """Invalid prompt."""
    code = "INVALID_PROMPT"
    message = "Prompt validation failed"


class QuestionGenerationFailedException(DomainException):
    """Question generation failed."""
    code = "QUESTION_GENERATION_FAILED"
    message = "Failed to generate clarifying questions"


class CacheException(DomainException):
    """Cache operation failed."""
    code = "CACHE_ERROR"
    message = "Cache operation failed"
