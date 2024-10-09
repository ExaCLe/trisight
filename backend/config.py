# config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"  # Default to SQLite for development

    class ConfigDict:
        env_file = ".env"  # Load environment variables from a .env file


settings = Settings()
