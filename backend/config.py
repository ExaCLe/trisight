# config.py
from pydantic import BaseSettings, AnyUrl


class Settings(BaseSettings):
    DATABASE_URL: AnyUrl = "sqlite:///./test.db"  # Default to SQLite for development

    class Config:
        env_file = ".env"  # Load environment variables from a .env file


settings = Settings()
