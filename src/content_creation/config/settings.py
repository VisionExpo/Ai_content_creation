from pydantic_settings import BaseSettings
from typing import Optional, List

class Settings(BaseSettings):
    # API Keys
    GEMINI_API_KEY: str
    HUGGINGFACE_API_KEY: Optional[str] = None
    STABILITY_API_KEY: Optional[str] = None

    # Server Configuration
    API_V1_PREFIX: str = "/api"
    PROJECT_NAME: str = "Social.AI - AI Content Creation API"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Generation Settings
    MAX_VIDEO_DURATION: int = 300  # Maximum video duration in seconds
    MIN_VIDEO_DURATION: int = 10   # Minimum video duration in seconds
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        env_prefix = ""

settings = Settings()
