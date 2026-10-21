from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    groq_api_key: str
    database_url: str
    allowed_origins: list[str]
    model_name: str

    model_config = {
        "env_file": Path(__file__).parent / ".env.local",
        "extra": "ignore",
    }


settings = Settings()