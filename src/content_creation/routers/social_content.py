from fastapi import APIRouter

router = APIRouter()

@router.get("/social_content")
def get_social_content(content_title: str, platform: str):
    return {
        "message": f"Generating social media content titled '{content_title}' for platform '{platform}'."
    }
