import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from src.content_creation.routers import ads, social_content, video

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Social.AI - AI Content Creation API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app will run on this port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Jinja2 Templates
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(ads.router, prefix="/api", tags=["Ad Generation"])
app.include_router(social_content.router, prefix="/api", tags=["Social Media Content"])
app.include_router(video.router, prefix="/api", tags=["AI Video Generation"])

# Global Exception Handlers
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

# Home route
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Ad Generation route
@app.get("/ad-generation")
async def ad_generation(request: Request):
    return templates.TemplateResponse("ad-generation.html", {"request": request})

# Social Content route
@app.get("/social-content")
async def social_content(request: Request):
    return templates.TemplateResponse("social-content.html", {"request": request})

# Video Generation route
@app.get("/video-generation")
async def video_generation(request: Request):
    return templates.TemplateResponse("video-generation.html", {"request": request})
