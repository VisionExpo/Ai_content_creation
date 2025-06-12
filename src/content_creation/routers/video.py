from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import logging
from typing import Optional
import google.generativeai as genai
from ..config.settings import settings
from ..utils.exceptions import GeminiAPIError, ValidationError

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize Gemini model once
try:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-pro")
    logger.info("Gemini model initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Gemini model: {str(e)}")
    model = None

class VideoConceptRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    duration: int = Field(default=30, ge=10, le=300)
    purpose: Optional[str] = Field(default="Product Demo Ad")
    target_audience: Optional[str] = Field(default="General audience")

def generate_video_script(prompt: str) -> str:
    """Generate video script using Gemini API"""
    if not model:
        raise GeminiAPIError("Gemini model not initialized")
        
    try:
        generation_config = {
            "temperature": 0.7,
            "top_p": 1,
            "top_k": 32,
            "max_output_tokens": 2048,
        }
        
        logger.info("Generating video script...")
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        if not response or not hasattr(response, 'text'):
            raise GeminiAPIError("Invalid response from Gemini API")
            
        text = response.text.strip()
        if not text:
            raise GeminiAPIError("Empty response from Gemini API")
            
        logger.info(f"Generated script of length: {len(text)}")
        return text
        
    except Exception as e:
        logger.error(f"Error generating script: {str(e)}")
        raise GeminiAPIError(f"Failed to generate script: {str(e)}")

@router.get("/videos")
async def get_videos(video_title: str, duration: int):
    """Handle GET requests for video generation"""
    try:
        # Basic validation
        if not video_title or not duration:
            raise ValidationError("Missing required parameters")
            
        # Clean title
        title = video_title.strip()
        if len(title) < 3:
            raise ValidationError("Title must be at least 3 characters long")
            
        # Create prompt
        prompt = f'''As a professional video producer, create a detailed {duration}-second video script for: "{title}"

Required sections:
1. Scene-by-scene breakdown with exact timestamps
2. Visual descriptions with camera angles and movements
3. Voice-over script
4. On-screen text
5. Transitions between scenes

Format for each scene:
Scene [X] ([start time] - [end time])
- Visuals: [detailed visual description]
- Audio: [voice-over script and sound design]
- Text: [on-screen text elements]
- Transition: [transition to next scene]

Make it engaging and professional, suitable for a high-end product video.'''
        
        # Generate script
        detailed_script = generate_video_script(prompt)
        
        return {
            "video_title": title,
            "duration": f"{duration} seconds",
            "purpose": "Product Demo Ad",
            "target_audience": "General audience",
            "detailed_script": detailed_script
        }
        
    except ValidationError as ve:
        logger.error(f"Validation error: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except GeminiAPIError as ge:
        logger.error(f"Gemini API error: {str(ge)}")
        raise HTTPException(status_code=500, detail=str(ge))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to generate video concept. Please try again."
        )
