from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings."""

    # API Keys
    anthropic_api_key: str = ""
    openai_api_key: str = ""

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True

    # CORS
    cors_origins: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ]

    # Application
    app_name: str = "The Griddler - COBOL SCR100 Parser"
    version: str = "0.1.0"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
