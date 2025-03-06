import os
import logging
import openai
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
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
class AdRequest(BaseModel):
    brand_name: str
    product_name: str
    target_audience: str
    key_features: list[str]
    tone: str  # e.g., "friendly", "professional", "funny"

def generate_ai_ad(brand_name: str, product_name: str, target_audience: str, key_features: list[str], tone: str):
    """Generate an AI-powered advertisement copy using OpenAI's GPT-3.5 model."""
    
    prompt = f"""
    Create a {tone} advertisement for a product.
    Brand: {brand_name}
    Product: {product_name}
    Target Audience: {target_audience}
    Key Features: {", ".join(key_features)}

    Make it engaging and concise.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )
        logger.info(f"OpenAI API response: {response}")  # Log the response for debugging
        if "choices" in response and len(response["choices"]) > 0:
            return response["choices"][0]["message"]["content"]
        else:
            raise HTTPException(status_code=500, detail="Unexpected response structure from OpenAI API.")

    except Exception as e:
        logger.error(f"Error generating ad with input: {brand_name}, {product_name}, {target_audience}, {key_features}, {tone}. Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating ad.")

# Define the API endpoint
@router.post("/generate_ad")
async def generate_ad(ad_request: AdRequest):
    """Endpoint to generate an ad using AI."""
    try:
        ad_copy = generate_ai_ad(
            ad_request.brand_name,
            ad_request.product_name,
            ad_request.target_audience,
            ad_request.key_features,
            ad_request.tone
        )
        return {"ad_copy": ad_copy}
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
