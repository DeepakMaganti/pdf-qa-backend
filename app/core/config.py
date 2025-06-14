from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    UPLOAD_DIR: str = "data/storage"
    CHROMA_DB_DIR: str = "data/chroma"
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    model_config = SettingsConfigDict(
        env_file=".env",       # Load from .env file
        case_sensitive=True,
        extra="allow"          # ✅ Accept extra env vars like HOST, PORT
    )

settings = Settings()
