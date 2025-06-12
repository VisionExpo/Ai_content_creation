from fastapi import APIRouter, Body, Request, HTTPException
from pydantic import BaseModel, Field
import logging
from typing import Optional
import google.generativeai as genai
from ..config.settings import settings
from ..utils.exceptions import GeminiAPIError, ValidationError, ConfigurationError

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize Gemini configuration with default model settings
genai.configure(api_key=settings.GEMINI_API_KEY)

# Define generation config
generation_config = {
    "temperature": 0.7,
    "top_p": 0.8,
    "top_k": 40,
    "max_output_tokens": 1000,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
]

class VideoConceptRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    duration: int = Field(default=30, ge=10, le=300)
    purpose: Optional[str] = Field(default="Product Demo Ad")
    target_audience: Optional[str] = Field(default="General audience")

async def call_gemini_api(prompt: str) -> str:
    """Call the Gemini API to generate video concept."""
    try:
        # Initialize the model for this request
        model = genai.GenerativeModel("gemini-pro")
        
        # Generate content
        response = model.generate_content(
            prompt,
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        
        if hasattr(response, 'text') and response.text:
            return response.text.strip()
        else:
            logger.error("No text in Gemini API response")
            raise GeminiAPIError("No text in response")
            
    except Exception as e:
        logger.error(f"Error calling Gemini API: {str(e)}")
        raise GeminiAPIError(f"Error calling Gemini API: {str(e)}")

@router.get("/videos")
async def get_videos(video_title: str, duration: int):
    """Handle GET requests for video generation"""
    try:
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
        
        # Create the video request
        video_request = VideoConceptRequest(
            title=trimmed_title,
            duration=duration,
            purpose="Product Demo Ad",
            target_audience="Runners, fitness enthusiasts, and young athletes"
        )
        
        # Generate the video concept
        prompt = (
            f"Create a detailed video script for a {duration}-second video about {video_request.title}.\n\n"
            f"Purpose: {video_request.purpose}\n"
            f"Target Audience: {video_request.target_audience}\n\n"
            "Please provide a scene-by-scene breakdown including:\n"
            "1. Timestamp for each scene\n"
            "2. Visual description\n"
            "3. Voiceover script\n"
            "4. Any on-screen text or graphics\n"
            "5. Transitions between scenes\n\n"
            "Format each scene as:\n"
            "Scene [number] ([time range])\n"
            "- Visuals: [description]\n"
            "- Audio: [voiceover/music description]\n"
            "- Text: [on-screen text if any]\n"
            "- Transition: [transition type if any]"
        )
        
        detailed_script = await call_gemini_api(prompt)
        
        return {
            "video_title": video_request.title,
            "duration": f"{video_request.duration} seconds",
            "purpose": video_request.purpose,
            "target_audience": video_request.target_audience,
            "detailed_script": detailed_script
        }
        
    except ValidationError as ve:
        logger.error(f"Validation error: {str(ve)}")
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(ve)}")
    except GeminiAPIError as ge:
        logger.error(f"Gemini API error: {str(ge)}")
        raise HTTPException(status_code=500, detail=str(ge))
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
