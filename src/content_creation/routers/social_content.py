import os
import logging
import google.generativeai as genai
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Set up the model
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 300,
}

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

def generate_fallback_content(request: SocialContentRequest) -> str:
    """Generate content without using external APIs as a fallback mechanism."""

    # Platform-specific templates
    templates = {
        "instagram": "✨ NEW PRODUCT ALERT! ✨\n\n{intro}\n\n{features}\n\n{special}\n\n{target}\n\n{hashtags}",
        "facebook": "🔥 INTRODUCING: {product_name} 🔥\n\n{intro}\n\n{features}\n\n{special}\n\n{target}\n\n{hashtags}",
        "twitter": "{intro} {features} {special} {target} {hashtags}",
        "linkedin": "🚀 Product Announcement 🚀\n\n{intro}\n\n{features}\n\n{special}\n\n{target}\n\n{hashtags}",
        "tiktok": "Check out the new {product_name}! 🤩\n{features}\n{special}\n{hashtags}"
    }

    # Emoji sets based on tone
    emojis = {
        "engaging": ["✨", "🔥", "👀", "🙌", "💯"],
        "professional": ["📊", "💼", "🚀", "📈", "✅"],
        "friendly": ["😊", "👋", "🤗", "💕", "👍"],
        "humorous": ["😂", "🤣", "😜", "🤪", "😎"],
        "excited": ["🤩", "🎉", "🔥", "💥", "⚡"],
        "formal": ["📝", "📋", "🔍", "📌", "🔖"]
    }

    # Hashtag templates
    hashtag_templates = {
        "instagram": ["#NewProduct", "#MustHave", "#{product_category}Life", "#{product_name}Launch", "#Innovation"],
        "facebook": ["#NewProduct", "#{product_category}", "#{product_name}", "#Innovation"],
        "twitter": ["#New", "#{product_category}", "#{product_name}"],
        "linkedin": ["#ProductLaunch", "#Innovation", "#{product_category}Industry", "#{product_name}"],
        "tiktok": ["#fyp", "#{product_category}Check", "#{product_name}Reveal", "#NewProductAlert"]
    }

    # Get the appropriate template and emoji set
    template = templates.get(request.platform.lower(), templates["instagram"])
    emoji_set = emojis.get(request.tone.lower(), emojis["engaging"])

    # Format product name
    product_name = request.product_name or "our new product"
    product_category = request.product_category or "product"

    # Create intro
    intro = f"Introducing {product_name}" + (f", our new {product_category}" if request.product_category else "") + "!"
    if request.include_emojis:
        intro = f"{emoji_set[0]} {intro} {emoji_set[1]}"

    # Format features
    features = ""
    if request.key_features:
        features = "Key Features:"
        for i, feature in enumerate(request.key_features):
            emoji = emoji_set[i % len(emoji_set)] if request.include_emojis else ""
            features += f"\n- {emoji} {feature}"

    # Format special features
    special = ""
    if request.special_features:
        special = f"Special Features: {request.special_features}"
        if request.include_emojis:
            special = f"{emoji_set[2]} {special}"

    # Format target audience
    target = ""
    if request.target_audience:
        target = f"Perfect for {request.target_audience}!"
        if request.include_emojis:
            target = f"{emoji_set[3]} {target}"

    # Format hashtags
    hashtags = ""
    if request.include_hashtags:
        hashtag_list = hashtag_templates.get(request.platform.lower(), hashtag_templates["instagram"])
        formatted_hashtags = []
        for tag in hashtag_list:
            if "{product_name}" in tag and request.product_name:
                tag = tag.replace("{product_name}", request.product_name.replace(" ", ""))
            elif "{product_category}" in tag and request.product_category:
                tag = tag.replace("{product_category}", request.product_category.replace(" ", ""))
            formatted_hashtags.append(tag)
        hashtags = " ".join(formatted_hashtags)

    # Format the final content
    content = template.format(
        intro=intro,
        product_name=product_name,
        features=features,
        special=special,
        target=target,
        hashtags=hashtags
    )

    # Truncate for Twitter
    if request.platform.lower() == "twitter" and len(content) > 280:
        content = content[:277] + "..."

    return content

def generate_social_content(request: SocialContentRequest):

    # Platform-specific templates
    templates = {
        "instagram": "✨ NEW PRODUCT ALERT! ✨\n\n{intro}\n\n{features}\n\n{special}\n\n{target}\n\n{hashtags}",
        "facebook": "🔥 INTRODUCING: {product_name} 🔥\n\n{intro}\n\n{features}\n\n{special}\n\n{target}\n\n{hashtags}",
        "twitter": "{intro} {features} {special} {target} {hashtags}",
        "linkedin": "🚀 Product Announcement 🚀\n\n{intro}\n\n{features}\n\n{special}\n\n{target}\n\n{hashtags}",
        "tiktok": "Check out the new {product_name}! 🤩\n{features}\n{special}\n{hashtags}"
    }

    # Emoji sets based on tone
    emojis = {
        "engaging": ["✨", "🔥", "👀", "🙌", "💯"],
        "professional": ["📊", "💼", "🚀", "📈", "✅"],
        "friendly": ["😊", "👋", "🤗", "💕", "👍"],
        "humorous": ["😂", "🤣", "😜", "🤪", "😎"],
        "excited": ["🤩", "🎉", "🔥", "💥", "⚡"],
        "formal": ["📝", "📋", "🔍", "📌", "🔖"]
    }

    # Hashtag templates
    hashtag_templates = {
        "instagram": ["#NewProduct", "#MustHave", "#{product_category}Life", "#{product_name}Launch", "#Innovation"],
        "facebook": ["#NewProduct", "#{product_category}", "#{product_name}", "#Innovation"],
        "twitter": ["#New", "#{product_category}", "#{product_name}"],
        "linkedin": ["#ProductLaunch", "#Innovation", "#{product_category}Industry", "#{product_name}"],
        "tiktok": ["#fyp", "#{product_category}Check", "#{product_name}Reveal", "#NewProductAlert"]
    }

    # Get the appropriate template and emoji set
    template = templates.get(request.platform.lower(), templates["instagram"])
    emoji_set = emojis.get(request.tone.lower(), emojis["engaging"])

    # Format product name
    product_name = request.product_name or "our new product"
    product_category = request.product_category or "product"

    # Create intro
    intro = f"Introducing {product_name}" + (f", our new {product_category}" if request.product_category else "") + "!"
    if request.include_emojis:
        intro = f"{emoji_set[0]} {intro} {emoji_set[1]}"

    # Format features
    features = ""
    if request.key_features:
        features = "Key Features:"
        for i, feature in enumerate(request.key_features):
            emoji = emoji_set[i % len(emoji_set)] if request.include_emojis else ""
            features += f"\n- {emoji} {feature}"

    # Format special features
    special = ""
    if request.special_features:
        special = f"Special Features: {request.special_features}"
        if request.include_emojis:
            special = f"{emoji_set[2]} {special}"

    # Format target audience
    target = ""
    if request.target_audience:
        target = f"Perfect for {request.target_audience}!"
        if request.include_emojis:
            target = f"{emoji_set[3]} {target}"

    # Format hashtags
    hashtags = ""
    if request.include_hashtags:
        hashtag_list = hashtag_templates.get(request.platform.lower(), hashtag_templates["instagram"])
        formatted_hashtags = []
        for tag in hashtag_list:
            if "{product_name}" in tag and request.product_name:
                tag = tag.replace("{product_name}", request.product_name.replace(" ", ""))
            elif "{product_category}" in tag and request.product_category:
                tag = tag.replace("{product_category}", request.product_category.replace(" ", ""))
            formatted_hashtags.append(tag)
        hashtags = " ".join(formatted_hashtags)

    # Format the final content
    content = template.format(
        intro=intro,
        product_name=product_name,
        features=features,
        special=special,
        target=target,
        hashtags=hashtags
    )

    # Truncate for Twitter
    if request.platform.lower() == "twitter" and len(content) > 280:
        content = content[:277] + "..."

    return content

def generate_social_content(request: SocialContentRequest):
    """Generate social media content using Google's Gemini API."""

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

    # Build the prompt for Gemini
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
        # Try to use Gemini API
        try:
            # Initialize the model
            model = genai.GenerativeModel(
                model_name="gemini-pro",
                generation_config=generation_config
            )

            # Generate content
            response = model.generate_content(prompt)
            logger.info(f"Gemini API response: {response}")

            # Check if the response has text
            if response.text:
                return response.text.strip()
            else:
                # If no text in response, use fallback
                logger.warning("No text in Gemini API response. Using fallback.")
                return generate_fallback_content(request)

        except Exception as api_error:
            # If Gemini API fails, log the error and use fallback
            logger.error(f"Error with Gemini API: {str(api_error)}")
            logger.info("Using fallback content generation mechanism")
            return generate_fallback_content(request)

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
