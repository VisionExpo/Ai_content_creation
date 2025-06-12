from fastapi import APIRouter, Body, Request, HTTPException
from pydantic import BaseModel, Field
import httpx
import logging
from typing import Optional
from ..config.settings import settings
from ..utils.exceptions import GeminiAPIError, ValidationError, ConfigurationError

router = APIRouter()
logger = logging.getLogger(__name__)

class VideoConceptRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    duration: int = Field(default=30, ge=10, le=300)
    purpose: Optional[str] = Field(default="Product Demo Ad")
    target_audience: Optional[str] = Field(default="General audience")

async def call_gemini_api(prompt: str) -> str:
    """Call the Gemini API to generate video concept."""
    if not settings.GEMINI_API_KEY:
        raise ConfigurationError("Gemini API key not configured")
    
    headers = {
        "Authorization": f"Bearer {settings.GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        # Format request according to Gemini API specifications
        request_data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 500,
                "topP": 0.8,
                "topK": 40
            }
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                settings.GEMINI_API_URL,
                headers=headers,
                json=request_data
            )
            
            if response.status_code != 200:
                logger.error(f"Gemini API error: {response.text}")
                raise GeminiAPIError(response.text)
            
            data = response.json()
            # Gemini API returns the response in a different format than OpenAI
            if "candidates" in data:
                return data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                logger.error(f"Unexpected Gemini API response structure: {data}")
                raise GeminiAPIError("Unexpected response structure from Gemini API")
                
    except httpx.HTTPError as e:
        logger.error(f"HTTP error occurred: {str(e)}")
        raise GeminiAPIError(f"HTTP error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise GeminiAPIError(f"Unexpected error: {str(e)}")

@router.get("/videos")
async def get_videos(video_title: str, duration: int):
    """Handle GET requests for video generation"""
    try:
        logger.info(f"Received video generation request with title: {video_title}, duration: {duration}")
        
        # Clean and validate title
        title = video_title.strip()
        if "Video Title:" in title:
            title = title.split("Video Title:")[1].strip()
        if "Duration:" in title:
            title = title.split("Duration:")[0].strip()
            
        # Trim the title to first 100 characters if it's too long
        trimmed_title = title[:100] if len(title) > 100 else title
        
        # If title was trimmed, log a warning
        if trimmed_title != title:
            logger.warning(f"Title was trimmed from {len(title)} to 100 characters")
        
        # Create a video request object
        video_request = VideoConceptRequest(
            title=trimmed_title,
            duration=duration,
            purpose="Product Demo Ad",
            target_audience="Runners, fitness enthusiasts, and young athletes"
        )
          # Generate the video concept
        prompt = (
            f"Generate a detailed video script outline (scene by scene) for a video titled '{video_request.title}' "
            f"with duration {video_request.duration} seconds. "
            f"The purpose is '{video_request.purpose}' and the target audience is '{video_request.target_audience}'. "
            "Include scene number, time range, visuals, voiceover, and text on screen if applicable."
        )

        logger.info(f"Generating video concept with prompt: {prompt}")
        
        detailed_script = await call_gemini_api(prompt)
        
        response = {
            "video_title": video_request.title,
            "duration": f"{video_request.duration} seconds",
            "purpose": video_request.purpose,
            "target_audience": video_request.target_audience,
            "detailed_script": detailed_script
        }
        
        return response
        
    except ValidationError as ve:
        logger.error(f"Validation error: {str(ve)}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid input: {str(ve)}"
        )
    except Exception as e:
        logger.error(f"Error generating video: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate video concept. Please try again."
        )

@router.post("/generate_video_concept")
async def generate_video_concept(
    request: Request,
    video_request: VideoConceptRequest = Body(...)
):
    """Generate a video concept using the Gemini API."""
    request_id = request.headers.get("X-Request-ID", "unknown")
    
    try:
        # Clean and validate title
        title = video_request.title.strip()
        if "Video Title:" in title:
            title = title.split("Video Title:")[1].strip()
        if "Duration:" in title:
            title = title.split("Duration:")[0].strip()
            
        # Update the video request with cleaned title
        video_request.title = title
        
        logger.info(
            "Generating video concept",
            extra={
                "request_id": request_id,
                "title": video_request.title,
                "duration": video_request.duration
            }
        )
        
        prompt = (
            f"Generate a detailed video script outline (scene by scene) for a video titled '{video_request.title}' "
            f"with duration {video_request.duration} seconds. "
            f"The purpose is '{video_request.purpose}' and the target audience is '{video_request.target_audience}'. "
            "Include scene number, time range, visuals, voiceover, and text on screen if applicable."
        )

        detailed_script = await call_gemini_api(prompt)

        response = {
            "video_title": video_request.title,
            "duration": f"{video_request.duration} seconds",
            "purpose": video_request.purpose,
            "target_audience": video_request.target_audience,
            "detailed_script": detailed_script
        }

        logger.info(
            "Video concept generated successfully",
            extra={"request_id": request_id}
        )

        return response
        
    except GeminiAPIError as e:
        logger.error(f"Gemini API error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    except ValidationError as ve:
        logger.error(f"Validation error: {str(ve)}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid input: {str(ve)}"
        )
    except Exception as e:
        logger.error(f"Error generating video concept: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate video concept. Please try again."
        )
