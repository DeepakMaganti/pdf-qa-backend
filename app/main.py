import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from app.core.config import settings
from app.api.router import qa, upload

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("App started")

# Initialize FastAPI app
app = FastAPI(
    title="PDF QA API",
    description="API for uploading PDFs and asking questions about their content using OpenAI and ChromaDB",
    version="1.0.0"
)

# CORS configuration (adjust origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use a specific origin like ["http://localhost:3000"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files (Frontend assets)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Include modular API routers
app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(qa.router, prefix="/api", tags=["Query"])

# Frontend home route
@app.get("/")
def serve_frontend():
    return FileResponse("frontend/index.html")

# Health check
@app.get("/health")
async def health():
    return JSONResponse(content={"status": "ok"})

# API metadata/info route
@app.get("/api/info")
async def api_info():
    return {"message": "Welcome to PDF QA API"}

# Routes to serve individual assets directly (optional if not handled via HTML)
@app.get("/styles.css")
async def get_styles():
    return FileResponse("frontend/styles.css")

@app.get("/script.js")
async def get_script():
    return FileResponse("frontend/script.js")

# Ensure required directories exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
