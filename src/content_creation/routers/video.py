from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
import logging
from typing import Optional
import google.generativeai as genai
from ..config.settings import settings
from ..utils.exceptions import GeminiAPIError, ValidationError

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize Gemini configuration
try:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    logger.info("Gemini API configured successfully")
except Exception as e:
    logger.error(f"Failed to configure Gemini API: {str(e)}")
    raise

class VideoConceptRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    duration: int = Field(
        default=30,
        ge=settings.MIN_VIDEO_DURATION,
        le=settings.MAX_VIDEO_DURATION
    )
    purpose: Optional[str] = Field(default="Product Demo Ad")
    target_audience: Optional[str] = Field(default="General audience")

def create_video_prompt(title: str, duration: int, purpose: str, target_audience: str) -> str:
    """Create a detailed prompt for video generation."""
    return f'''Create a professional {duration}-second video script for: "{title}"

Purpose: {purpose}
Target Audience: {target_audience}

Please provide a detailed breakdown including:
1. Scene-by-scene description with exact timestamps
2. Visual descriptions (camera angles, movements, composition)
3. Voice-over script with tone and pacing
4. On-screen text and graphics
5. Music and sound design suggestions
6. Transitions between scenes

Format each scene as:
Scene [number] ([start time] - [end time])
- Visuals: [detailed visual description]
- Audio: [voice-over script and sound design]
- Text: [on-screen text content]
- Transition: [transition type]

Make the script engaging and professional, focusing on high production value.'''

def generate_video_script(prompt: str) -> str:
    """Generate video script using Gemini API."""
    try:
        # Configure generation settings
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 2048,
        }

        # Initialize model
        model = genai.GenerativeModel("gemini-pro")
        
        # Generate content
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        if not response or not hasattr(response, 'text'):
            raise GeminiAPIError("Invalid response from Gemini API")
        
        text = response.text.strip()
        if not text:
            raise GeminiAPIError("Empty response from Gemini API")
            
        return text
        
    except Exception as e:
        logger.error(f"Error generating video script: {str(e)}", exc_info=True)
        raise GeminiAPIError(f"Failed to generate video script: {str(e)}")

@router.get("/videos")
async def get_videos(video_title: str, duration: int):
    """Handle GET requests for video generation."""
    try:
        # Clean and validate title
        title = video_title.strip()
        if not title:
            raise ValidationError("Video title cannot be empty")
            
        # Remove any metadata from the title
        if "Video Title:" in title:
            title = title.split("Video Title:")[1].strip()
        if "Duration:" in title:
            title = title.split("Duration:")[0].strip()
        
        # Validate duration
        if duration < settings.MIN_VIDEO_DURATION or duration > settings.MAX_VIDEO_DURATION:
            raise ValidationError(
                f"Duration must be between {settings.MIN_VIDEO_DURATION} and {settings.MAX_VIDEO_DURATION} seconds"
            )
        
        # Create prompt
        prompt = create_video_prompt(
            title=title,
            duration=duration,
            purpose="Product Demo Ad",
            target_audience="General audience"
        )
        
        # Generate script
        detailed_script = generate_video_script(prompt)
        
        # Return response
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
