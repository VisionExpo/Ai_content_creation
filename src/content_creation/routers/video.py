from fastapi import APIRouter, Body, Request
from pydantic import BaseModel, Field
import httpx
import logging
from ..config.settings import settings
from ..utils.exceptions import GeminiAPIError, ValidationError, ConfigurationError
from typing import Optional

router = APIRouter()
logger = logging.getLogger(__name__)

class VideoConceptRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    duration: int = Field(default=30, ge=10, le=300)
    purpose: Optional[str] = Field(default="Product Demo Ad")
    target_audience: Optional[str] = Field(default="General audience")

async def call_gemini_api(prompt: str) -> str:
    if not settings.GEMINI_API_KEY:
        raise ConfigurationError("Gemini API key not configured")
    
    headers = {
        "Authorization": f"Bearer {settings.GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                settings.GEMINI_API_URL,
                headers=headers,
                json={
                    "prompt": prompt,
                    "max_tokens": 500,
                    "temperature": 0.7
                }
            )
            
            if response.status_code != 200:
                logger.error(f"Gemini API error: {response.text}")
                raise GeminiAPIError(response.text)
                
            data = response.json()
            return data.get("choices", [{}])[0].get("text", "")
            
    except httpx.HTTPError as e:
        logger.error(f"HTTP error occurred: {str(e)}")
        raise GeminiAPIError(f"HTTP error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise GeminiAPIError(f"Unexpected error: {str(e)}")

@router.post("/generate_video_concept")
async def generate_video_concept(
    request: Request,
    video_request: VideoConceptRequest = Body(...)
):
    request_id = request.headers.get("X-Request-ID", "unknown")
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
