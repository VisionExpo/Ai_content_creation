import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from src.content_creation.routers import ads, social_content, video
from src.content_creation.config.settings import settings
from src.content_creation.utils.logging import setup_logging
from src.content_creation.middleware.request_tracking import RequestTrackingMiddleware
from src.content_creation.utils.exceptions import APIError

# Set up logging
logger = setup_logging()

# Verify environment
from src.content_creation.utils.startup import verify_environment
startup_errors = verify_environment()
if startup_errors:
    for error in startup_errors:
        logger.error(f"Startup Error: {error}")
    raise SystemExit(1)

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json")

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestTrackingMiddleware)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Jinja2 Templates
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(ads.router, prefix=settings.API_V1_PREFIX, tags=["Ad Generation"])
app.include_router(social_content.router, prefix=settings.API_V1_PREFIX, tags=["Social Media Content"])
app.include_router(video.router, prefix=settings.API_V1_PREFIX, tags=["AI Video Generation"])

# Exception handlers
@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    logger.error(
        "API error occurred",
        extra={
            "request_id": getattr(request.state, "request_id", "unknown"),
            "status_code": exc.status_code,
            "detail": exc.detail
        }
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(
        "Unexpected error occurred",
        extra={
            "request_id": getattr(request.state, "request_id", "unknown"),
            "error": str(exc)
        }
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Home route
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

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
