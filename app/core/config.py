from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    BOT_TOKEN: str
    DATABASE_URL: str
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

config = Settings()