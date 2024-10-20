# config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"  # Default to SQLite for development
    SECRET_KEY: str = "secret"  # Default to a simple secret key
    FRONTEND_URL: str = "http://localhost:3000"
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""

    class ConfigDict:
        env_file = ".env"  # Load environment variables from a .env file


settings = Settings()
