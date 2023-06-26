# shortener_app/config.py

from functools import lru_cache

from pydantic import BaseSettings

# creates Settings as a child of BaseSettings and assings values
class Settings(BaseSettings):
    env_name: str = "Local"
    base_url: str = "http://localhost:8000"
    db_url: str = "sqlite:///./shortener.db"
    
    # loads the default settings from the .env file
    class Config:
        env_file = ".env"

# function returns settings, lru cache is used here to cache 'em
@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings for: {settings.env_name}")
    return settings
