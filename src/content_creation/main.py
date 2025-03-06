import logging
from fastapi import FastAPI, HTTPException, Request

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

# Include routers
app.include_router(ads.router, prefix="/api", tags=["Ad Generation"])
app.include_router(social_content.router, prefix="/api", tags=["Social Media Content"])
app.include_router(video.router, prefix="/api", tags=["AI Video Generation"])

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."},
    )

@app.get("/")
def home():
    return {"message": "Welcome to the AI Content Creation API!"}
