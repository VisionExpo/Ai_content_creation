import logging
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from src.content_creation.routers import ads, social_content, video

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Content Creation")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.include_router(ads.router, prefix="/api/ads", tags=["Ad Generation"])
app.include_router(social_content.router, prefix="/api/social_content", tags=["Social Media Content"])
app.include_router(video.router, prefix="/api/video", tags=["AI Video Generation"])

@app.get("/")
async def home(request: Request):
    """
    Home route that renders the index page.
    """
    try:
        return templates.TemplateResponse("index.html", {"request": request, "title": "AI Content Creation"})
    except Exception as e:
        logger.error(f"Error rendering index page: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
