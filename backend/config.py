# config.py
from pydantic_settings import BaseSettings
from pydantic import AnyUrl


class Settings(BaseSettings):
    DATABASE_URL: AnyUrl = "sqlite:///./test.db"  # Default to SQLite for development

    class Config:
        env_file = ".env"  # Load environment variables from a .env file


settings = Settings()
