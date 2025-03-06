import os
from pathlib import Path
import logging

# Logging configuration
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(levelname)s]: %(message)s')


project_name = "content_creation"

# List of files and folders to create based on user input
list_of_files = []
user_files = [
    ".github/workflows/.gitkeep",
    f"src/{project_name}/main.py",  
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/constants/__init__.py",
    f"src/{project_name}/routers/__init__.py",
    f"src/{project_name}/routers/ads.py",  
    f"src/{project_name}/routers/social_content.py", 
    f"src/{project_name}/routers/video.py",  
    "config/config.yaml",
    "params.yaml",
    "requirements.txt",
    "setup.py",
    "research/trials.ipynb",
    "templates/index.html",
    "templates/ad-generation.html",
    "templates/social-content.html",
    "templates/video-generation.html",
    "templates/results.html",
    "static/css/style.css",
    "static/js/script.js",
    "static/images/.gitkeep",

    "static/images/.gitkeep",
    "static/images/.gitkeep",
    "static/images/.gitkeep",
    "static/images/.gitkeep",
    "static/images/.gitkeep",
]

# Create directories and files
for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir:
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file: {filename}")

    if not filepath.exists() or filepath.stat().st_size == 0:
        with open(filepath, "w") as f:
            pass
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")
