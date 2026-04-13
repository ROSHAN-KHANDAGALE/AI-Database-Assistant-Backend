from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    groq_api_key: str
    database_url: str
    allowed_origins: list[str]
    model_name: str

    model_config = {
        "env_file": Path(__file__).parent / ".env.local"
    }

settings = Settings()