from typing import List
import logging
from pathlib import Path
import google.generativeai as genai
from ..config.settings import settings

logger = logging.getLogger(__name__)

def verify_environment() -> List[str]:
    """Verify all required environment variables and configurations are set."""
    errors = []
    
    # Check API keys
    if not settings.GEMINI_API_KEY:
        errors.append("GEMINI_API_KEY is not set in environment")
    else:
        # Test Gemini API configuration
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-pro")
            logger.info("Gemini API configured successfully")
        except Exception as e:
            errors.append(f"Failed to configure Gemini API: {str(e)}")
    
    # Check required directories exist
    required_dirs = [
        "static/images/generated",
        "templates"
    ]
    
    for dir_path in required_dirs:
        path = Path(dir_path)
        if not path.exists():
            try:
                path.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created directory: {dir_path}")
            except Exception as e:
                errors.append(f"Failed to create directory {dir_path}: {str(e)}")
    
    return errors
