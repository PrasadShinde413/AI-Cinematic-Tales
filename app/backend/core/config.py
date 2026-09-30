import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Cultural Screenplay Adaptation Studio"
    # For MVP, we'll use a local SQLite if Postgres is not explicitly available, 
    # but the requirement states PostgreSQL. We'll default to SQLite for instant local execution
    # and allow overriding via env var for Postgres.
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./studio.db")
    
    # ChromaDB path
    CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIR", "./chroma_data")
    
    # Ollama default model
    LLM_MODEL: str = os.getenv("LLM_MODEL", "llama3")
    
    # Image Generation API (Mock setup)
    IMAGE_API_KEY: str = os.getenv("IMAGE_API_KEY", "")

settings = Settings()
