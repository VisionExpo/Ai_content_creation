import os
import logging
import requests
import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Hugging Face API URL
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

# Headers for Hugging Face API
headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}" if HUGGINGFACE_API_KEY else "",
    "Content-Type": "application/json"
}

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
    """Generate an AI-powered advertisement copy using Hugging Face's API."""

    prompt = f"""<s>[INST]
    Create a {tone} advertisement for a product.
    Brand: {brand_name}
    Product: {product_name}
    Target Audience: {target_audience}
    Key Features: {", ".join(key_features)}

    Make it engaging and concise.
    [/INST]</s>
    """

    try:
        # Try to use Hugging Face API
        try:
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 150,
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "do_sample": True
                }
            }

            # Make the API request
            response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload)
            logger.info(f"Hugging Face API response status: {response.status_code}")

            # Check if the request was successful
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Hugging Face API response: {result}")

                # Extract the generated text
                if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
                    # Extract just the response part (after the prompt)
                    generated_text = result[0]["generated_text"]
                    # Remove the prompt part if it's included in the response
                    if "[/INST]" in generated_text:
                        generated_text = generated_text.split("[/INST]")[1].strip()
                    return generated_text
                else:
                    # If response structure is unexpected, use fallback
                    logger.warning("Unexpected response structure from Hugging Face API. Using fallback.")
                    return generate_fallback_ad(brand_name, product_name, target_audience, key_features, tone)
            else:
                # If API returns an error, use fallback
                logger.error(f"Hugging Face API error: {response.text}")
                return generate_fallback_ad(brand_name, product_name, target_audience, key_features, tone)

        except Exception as api_error:
            # If Hugging Face API fails, log the error and use fallback
            logger.error(f"Error with Hugging Face API: {str(api_error)}")
            logger.info("Using fallback ad generation mechanism")
            return generate_fallback_ad(brand_name, product_name, target_audience, key_features, tone)

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
