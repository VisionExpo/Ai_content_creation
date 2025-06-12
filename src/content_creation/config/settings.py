from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Keys
    GEMINI_API_KEY: str
    HUGGINGFACE_API_KEY: Optional[str] = None
    STABILITY_API_KEY: Optional[str] = None
      # API Endpoints
    GEMINI_API_URL: str = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"
    
    # Server Configuration
    API_V1_PREFIX: str = "/api"
    PROJECT_NAME: str = "Social.AI - AI Content Creation API"
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra fields in the environment

settings = Settings()
