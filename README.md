# AI Content Creation

## Overview
This project is an AI Content Creation API built with FastAPI. It provides endpoints for generating videos, social media content, and ads.

## Installation
To install the required dependencies, run:
```
pip install -r requirements.txt
```

## Usage
To start the API, run:
```
uvicorn src.content_creation.main:app --reload
```

## API Endpoints
- **GET /api/videos**: Generate a video.
  - **Parameters**: 
    - `video_title`: Title of the video.
    - `duration`: Duration of the video in seconds.
  
- **GET /api/social_content**: Generate social media content.
  - **Parameters**: 
    - `content_title`: Title of the content.
    - `platform`: The platform for which the content is generated.

- **GET /api/ads**: Generate an ad.
  - **Parameters**: 
    - `ad_title`: Title of the ad.
    - `target_audience`: The target audience for the ad.

## Logging
The application uses logging to track events and errors. Logs are output to the console.

## License
This project is licensed under the MIT License.
