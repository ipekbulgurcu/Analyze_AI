import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application settings configuration using Pydantic.
    Loads variables from .env file or environment variables.
    """
    APP_NAME: str = "Local RAG Service"
    API_V1_STR: str = "/api/v1"
    
    # LLM Settings
    OLLAMA_BASE_URL: str = "http://127.0.0.1:11434"
    LLM_MODEL: str = "gpt-oss:20b"  # Updated to match installed model
    
    # Vector DB Settings
    CHROMA_PERSIST_DIRECTORY: str = "data/chroma_db"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2" # Using a lightweight model for embeddings
    
    # Text Splitter Settings
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    class Config:
        env_file = ".env"

settings = Settings()
