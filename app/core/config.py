from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    UPLOAD_DIR: str = "data/storage"
    CHROMA_DB_DIR: str = "data/chroma"
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    class Config:
        env_file = ".env"  # Optional: will use this file if available (for local dev)
        case_sensitive = True

settings = Settings()
