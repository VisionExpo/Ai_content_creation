from fastapi import APIRouter

router = APIRouter()

@router.get("/videos")
def get_videos(video_title: str, duration: int):
    return {
        "message": f"Generating video titled '{video_title}' with duration {duration} seconds."
    }
