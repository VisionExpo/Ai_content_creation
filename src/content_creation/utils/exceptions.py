class APIError(Exception):
    """Base class for API-related exceptions."""
    pass

class ValidationError(APIError):
    """Exception raised for validation errors."""
    pass

class GeminiAPIError(APIError):
    """Exception raised for Gemini API-related errors."""
    pass

class ConfigurationError(APIError):
    """Exception raised for configuration-related errors."""
    pass
