from fastapi import HTTPException

class APIError(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class GeminiAPIError(APIError):
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=f"Gemini API error: {detail}")

class ValidationError(APIError):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=f"Validation error: {detail}")

class ConfigurationError(APIError):
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=f"Configuration error: {detail}")
