from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import logging
from typing import Optional
import google.generativeai as genai
from ..config.settings import settings

router = APIRouter()
logger = logging.getLogger(__name__)

# Basic Gemini configuration
genai.configure(api_key=settings.GEMINI_API_KEY)

class VideoConceptRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    duration: int = Field(default=30, ge=10, le=300)
    purpose: Optional[str] = Field(default="Product Demo Ad")
    target_audience: Optional[str] = Field(default="General audience")

def generate_video_script(title: str, duration: int) -> str:
    """Generate video script using Gemini API."""
    try:
        model = genai.GenerativeModel("gemini-pro")
        
        prompt = f'''Create a {duration}-second video script for: "{title}"

Please provide:
1. Scene-by-scene breakdown with timestamps
2. Visual descriptions and camera angles
3. Voice-over script
4. On-screen text details
5. Scene transitions

Format each scene as:
Scene [X] ([timestamp])
- Visual: [description]
- Audio: [voice-over]
- Text: [on-screen text]
- Transition: [type]'''

        response = model.generate_content(prompt)
        
        if response and hasattr(response, 'text'):
            return response.text.strip()
        else:
            raise Exception("Failed to generate response")
            
    except Exception as e:
        logger.error(f"Error generating script: {str(e)}")
        raise

@router.get("/videos")
async def get_videos(video_title: str, duration: int):
    """Handle GET requests for video generation."""
    try:
        # Input validation
        title = video_title.strip()
        if not title:
            raise HTTPException(status_code=400, detail="Video title is required")
            
        if duration < 10 or duration > 300:
            raise HTTPException(
                status_code=400,
                detail="Duration must be between 10 and 300 seconds"
            )
        
        # Generate script
        script = generate_video_script(title, duration)
        
        return {
            "video_title": title,
            "duration": f"{duration} seconds",
            "purpose": "Product Demo Ad",
            "target_audience": "General audience",
            "detailed_script": script
        }
        
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error in video generation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to generate video concept. Please try again."
        )
