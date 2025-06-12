from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import logging
from typing import Optional
import google.generativeai as genai
from ..config.settings import settings
import asyncio
from concurrent.futures import ThreadPoolExecutor

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize Gemini API with just the API key
genai.configure(api_key=settings.GEMINI_API_KEY)

class VideoConceptRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    duration: int = Field(default=30, ge=10, le=300)
    purpose: Optional[str] = Field(default="Product Demo Ad")
    target_audience: Optional[str] = Field(default="General audience")

def generate_content_sync(prompt: str) -> str:
    """Synchronous function to generate content using Gemini API."""
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        if response and hasattr(response, 'text'):
            return response.text.strip()
        raise Exception("No valid response from Gemini API")
    except Exception as e:
        logger.error(f"Error generating content: {str(e)}")
        raise

async def generate_content_async(prompt: str) -> str:
    """Asynchronous wrapper for generating content."""
    with ThreadPoolExecutor() as executor:
        try:
            return await asyncio.get_event_loop().run_in_executor(
                executor, generate_content_sync, prompt
            )
        except Exception as e:
            logger.error(f"Failed to generate content: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to generate video concept. Please try again."
            )

@router.get("/videos")
async def get_videos(video_title: str, duration: int):
    """Handle GET requests for video generation"""
    try:
        # Basic input validation
        if not video_title or not duration:
            raise HTTPException(status_code=400, detail="Missing required parameters")
            
        # Clean title
        title = video_title.strip()
        
        # Create prompt
        prompt = f'''
Create a detailed {duration}-second video script for: {title}

Please provide:
1. Scene-by-scene breakdown with specific timestamps
2. Visual descriptions including camera angles
3. Voice-over script
4. On-screen text
5. Transitions between scenes

Format each scene as:
Scene [number] ([timestamp])
- Visual description
- Voice-over
- Text overlay
- Transition
'''
        
        # Generate content asynchronously
        result = await generate_content_async(prompt)
        
        return {
            "video_title": title,
            "duration": f"{duration} seconds",
            "purpose": "Product Demo Ad",
            "target_audience": "General audience",
            "detailed_script": result
        }
        
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error in video generation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to generate video concept. Please try again."
        )
