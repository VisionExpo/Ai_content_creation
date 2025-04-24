import os
import logging
import base64
import google.generativeai as genai
import requests
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

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

# Create directory for storing images if it doesn't exist
STATIC_DIR = Path("static/images/generated")
STATIC_DIR.mkdir(parents=True, exist_ok=True)

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
    generate_image: Optional[bool] = False
    image_prompt: Optional[str] = None

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

def generate_ai_image(prompt: str) -> str:
    """Generate an image using Stability AI API and return the path to the saved image."""
    try:
        if not STABILITY_API_KEY:
            logger.warning("Stability API key is missing. Cannot generate image.")
            return None

        # For testing purposes, if no API key is available, generate a placeholder image
        if STABILITY_API_KEY.strip() == "":
            logger.warning("Using placeholder image generation since no Stability API key is provided")
            return create_placeholder_image(prompt)

        # Prepare the API request
        url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

        headers = {
            "Authorization": f"Bearer {STABILITY_API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        body = {
            "text_prompts": [
                {
                    "text": prompt,
                    "weight": 1.0
                }
            ],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30
        }

        # Make the API request
        logger.info(f"Sending image generation request to Stability AI with prompt: {prompt}")
        response = requests.post(url, headers=headers, json=body)

        if response.status_code != 200:
            logger.error(f"Error generating image: {response.status_code} - {response.text}")
            # Fall back to placeholder image
            return create_placeholder_image(prompt)

        data = response.json()

        # Save the image
        if "artifacts" in data and len(data["artifacts"]) > 0:
            artifact = data["artifacts"][0]
            image_data = base64.b64decode(artifact["base64"])

            # Generate a unique filename
            import time
            import hashlib
            timestamp = int(time.time())
            filename = f"image_{timestamp}_{hashlib.md5(prompt.encode()).hexdigest()[:8]}.png"
            image_path = STATIC_DIR / filename

            # Save the image
            with open(image_path, "wb") as f:
                f.write(image_data)

            # Return the relative path to the image
            return f"/static/images/generated/{filename}"
        else:
            logger.error("No image data in response")
            return create_placeholder_image(prompt)

    except Exception as e:
        logger.error(f"Error generating image: {str(e)}")
        return create_placeholder_image(prompt)

def create_placeholder_image(prompt: str) -> str:
    """Generate a placeholder image with text when API is not available."""
    try:
        # Import necessary libraries
        from PIL import Image, ImageDraw, ImageFont
        import textwrap
        import time
        import hashlib
        import os

        # Create a unique filename
        timestamp = int(time.time())
        filename = f"placeholder_{timestamp}_{hashlib.md5(prompt.encode()).hexdigest()[:8]}.png"
        image_path = STATIC_DIR / filename

        # Create a blank image
        width, height = 800, 600
        background_color = (240, 240, 240)  # Light gray
        text_color = (60, 60, 60)  # Dark gray

        image = Image.new('RGB', (width, height), background_color)
        draw = ImageDraw.Draw(image)

        # Try to load a font, use default if not available
        try:
            # Try to find a system font
            system_fonts = [
                "arial.ttf",
                "Arial.ttf",
                "Verdana.ttf",
                "DejaVuSans.ttf",
                "Tahoma.ttf",
                "calibri.ttf"
            ]

            font = None
            for font_name in system_fonts:
                try:
                    font = ImageFont.truetype(font_name, 24)
                    break
                except IOError:
                    continue

            if font is None:
                font = ImageFont.load_default()

        except Exception:
            font = ImageFont.load_default()

        # Draw a border
        border_width = 4
        draw.rectangle(
            [(border_width, border_width), (width - border_width, height - border_width)],
            outline=(180, 180, 180),
            width=border_width
        )

        # Add title
        title = "Image Placeholder"
        title_font_size = 36
        try:
            title_font = ImageFont.truetype(font.path, title_font_size)
        except:
            title_font = font

        title_width = draw.textlength(title, font=title_font)
        draw.text(((width - title_width) / 2, 50), title, font=title_font, fill=text_color)

        # Add prompt text with wrapping
        prompt_lines = textwrap.wrap(f"Prompt: {prompt}", width=40)
        y_position = 150
        for line in prompt_lines:
            line_width = draw.textlength(line, font=font)
            draw.text(((width - line_width) / 2, y_position), line, font=font, fill=text_color)
            y_position += 30

        # Add note about API key
        note = "Image generation requires a valid Stability API key."
        note_width = draw.textlength(note, font=font)
        draw.text(((width - note_width) / 2, height - 100), note, font=font, fill=text_color)

        # Save the image
        image.save(image_path)

        return f"/static/images/generated/{filename}"

    except Exception as e:
        logger.error(f"Error generating placeholder image: {str(e)}")
        return None

# Define the API endpoints
@router.post("/social_content")
async def create_social_content(request: SocialContentRequest):
    """Endpoint to generate social media content using AI."""
    try:
        # First generate the text content
        content = generate_social_content(request)
        response_data = {"message": content, "platform": request.platform}

        # Generate image if requested
        if request.generate_image:
            try:
                # Create image prompt if not provided
                image_prompt = request.image_prompt
                if not image_prompt:
                    # Use product details to create a default image prompt
                    product_desc = f"{request.product_name}" if request.product_name else request.content_title
                    category_desc = f" {request.product_category}" if request.product_category else ""
                    features_desc = ""
                    if request.key_features and len(request.key_features) > 0:
                        features_desc = f" with {', '.join(request.key_features[:2])}"

                    image_prompt = f"Professional product photo of {product_desc}{category_desc}{features_desc}, studio lighting, high quality, detailed"

                # Generate the image
                logger.info(f"Generating image with prompt: {image_prompt}")
                image_path = generate_ai_image(image_prompt)

                # Add image data to response if successful
                if image_path:
                    response_data["image_url"] = image_path
                    response_data["image_prompt"] = image_prompt
                    logger.info(f"Image generated successfully: {image_path}")
                else:
                    logger.warning("Image generation returned None")
            except Exception as img_error:
                # Log the error but continue with text content
                logger.error(f"Error during image generation: {str(img_error)}")
                # We don't add image data to the response, but we still return the text content

        return response_data
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
    except Exception as e:
        logger.error(f"Unexpected error in create_social_content: {str(e)}")
        return JSONResponse(status_code=500, content={"detail": f"An error occurred: {str(e)}"})

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
    include_emojis: Optional[bool] = True,
    generate_image: Optional[bool] = False,
    image_prompt: Optional[str] = None
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
            include_emojis=include_emojis,
            generate_image=generate_image,
            image_prompt=image_prompt
        )

        # First generate the text content
        content = generate_social_content(request)
        response_data = {"message": content, "platform": platform}

        # Generate image if requested
        if generate_image:
            try:
                # Create image prompt if not provided
                if not image_prompt:
                    # Use product details to create a default image prompt
                    product_desc = f"{product_name}" if product_name else content_title
                    category_desc = f" {product_category}" if product_category else ""
                    features_desc = ""
                    if key_features_list and len(key_features_list) > 0:
                        features_desc = f" with {', '.join(key_features_list[:2])}"

                    image_prompt = f"Professional product photo of {product_desc}{category_desc}{features_desc}, studio lighting, high quality, detailed"

                # Generate the image
                logger.info(f"Generating image with prompt: {image_prompt}")
                image_path = generate_ai_image(image_prompt)

                # Add image data to response if successful
                if image_path:
                    response_data["image_url"] = image_path
                    response_data["image_prompt"] = image_prompt
                    logger.info(f"Image generated successfully: {image_path}")
                else:
                    logger.warning("Image generation returned None")
            except Exception as img_error:
                # Log the error but continue with text content
                logger.error(f"Error during image generation: {str(img_error)}")
                # We don't add image data to the response, but we still return the text content

        return response_data
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
    except Exception as e:
        logger.error(f"Unexpected error in get_social_content: {str(e)}")
        return JSONResponse(status_code=500, content={"detail": f"An error occurred: {str(e)}"})
