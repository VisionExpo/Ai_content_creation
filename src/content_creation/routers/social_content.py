import os
import logging
import openai
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Verify API key is loaded
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key is missing. Ensure it is set in the .env file.")

# Initialize OpenAI API key
openai.api_key = OPENAI_API_KEY

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI router
router = APIRouter()

# Define the request model
class SocialContentRequest(BaseModel):
    content_title: str
    platform: str
    product_name: Optional[str] = None
    product_category: Optional[str] = None
    key_features: Optional[List[str]] = None
    special_features: Optional[str] = None
    target_audience: Optional[str] = None
    tone: Optional[str] = "engaging"
    include_hashtags: Optional[bool] = True
    include_emojis: Optional[bool] = True

def generate_social_content(request: SocialContentRequest):
    """Generate social media content using OpenAI's GPT model."""

    # Create platform-specific instructions
    platform_instructions = {
        "instagram": "Create an engaging Instagram post with emojis and relevant hashtags. Keep it visually descriptive and appealing.",
        "facebook": "Create a Facebook post that's informative and engaging. Include a clear call-to-action.",
        "twitter": "Create a concise Twitter post within 280 characters. Use hashtags sparingly but effectively.",
        "linkedin": "Create a professional LinkedIn post that highlights business value and industry relevance.",
        "tiktok": "Create a trendy TikTok caption that's catchy, uses trending phrases, and includes relevant hashtags."
    }

    # Build the features list if provided
    features_text = ""
    if request.key_features:
        features_text = "Key Features:\n" + "\n".join([f"- {feature}" for feature in request.key_features])

    # Build the special features text if provided
    special_features_text = ""
    if request.special_features:
        special_features_text = f"Special Features: {request.special_features}"

    # Build the product info if provided
    product_info = ""
    if request.product_name:
        product_info += f"Product Name: {request.product_name}\n"
    if request.product_category:
        product_info += f"Product Category: {request.product_category}\n"

    # Build the audience info if provided
    audience_info = ""
    if request.target_audience:
        audience_info = f"Target Audience: {request.target_audience}"

    # Build the prompt
    prompt = f"""
    {platform_instructions.get(request.platform.lower(), "Create a social media post")}

    Content Title/Topic: {request.content_title}
    {product_info}
    {features_text}
    {special_features_text}
    {audience_info}
    Tone: {request.tone}

    {"Include relevant hashtags." if request.include_hashtags else "Do not include hashtags."}
    {"Use appropriate emojis to enhance engagement." if request.include_emojis else "Do not use emojis."}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7
        )
        logger.info(f"OpenAI API response for social content: {response}")

        if "choices" in response and len(response["choices"]) > 0:
            return response["choices"][0]["message"]["content"]
        else:
            raise HTTPException(status_code=500, detail="Unexpected response structure from OpenAI API.")

    except Exception as e:
        logger.error(f"Error generating social content: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating social content.")

# Define the API endpoints
@router.post("/social_content")
async def create_social_content(request: SocialContentRequest):
    """Endpoint to generate social media content using AI."""
    try:
        content = generate_social_content(request)
        return {"message": content, "platform": request.platform}
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

# Keep the GET endpoint for backward compatibility
@router.get("/social_content")
async def get_social_content(
    content_title: str,
    platform: str,
    product_name: Optional[str] = None,
    product_category: Optional[str] = None,
    key_features: Optional[str] = None,
    special_features: Optional[str] = None,
    target_audience: Optional[str] = None,
    tone: Optional[str] = "engaging",
    include_hashtags: Optional[bool] = True,
    include_emojis: Optional[bool] = True
):
    """Endpoint to generate social media content using AI (GET method)."""
    try:
        # Parse key_features from comma-separated string to list
        key_features_list = None
        if key_features:
            key_features_list = [feature.strip() for feature in key_features.split(',') if feature.strip()]

        # Create request object
        request = SocialContentRequest(
            content_title=content_title,
            platform=platform,
            product_name=product_name,
            product_category=product_category,
            key_features=key_features_list,
            special_features=special_features,
            target_audience=target_audience,
            tone=tone,
            include_hashtags=include_hashtags,
            include_emojis=include_emojis
        )

        content = generate_social_content(request)
        return {"message": content, "platform": platform}
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
