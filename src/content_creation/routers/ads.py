from fastapi import APIRouter

router = APIRouter()

@router.get("/ads")
def get_ads(ad_title: str, target_audience: str):
    return {
        "message": f"Generating ad titled '{ad_title}' for target audience '{target_audience}'."
    }
