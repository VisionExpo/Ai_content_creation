from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from src.content_creation.routes import ads, social_content, video

app = FastAPI(title="AI Content Creation")

app.mount("/static", StaticFiles(directory="src/content_creation/static"), name="static")

templates = Jinja2Templates(directory="src/content_creation/templates")

app.include_router(ads.router, prefix="/api/ads", tags=["Ad Generation"])
app.include_router(social_content.router, prefix="/api/social_content", tags=["Social Media Content"])
app.include_router(video.router, prefix="/api/video", tags=["AI Video Generation"])

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "AI Content Creation"})
