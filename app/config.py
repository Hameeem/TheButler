import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "TheButler"
    VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./thebutler.db")
    
    # LLM Keys
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY", "")
    
    # Defaults
    DEFAULT_USER_EMAIL: str = "hameem@example.com"
    DEFAULT_USER_NAME: str = "Hameem"
    APPLICATION_MODE: str = "APPROVAL_REQUIRED"  # MANUAL, APPROVAL_REQUIRED, AUTOMATIC
    DAILY_APPLICATION_LIMIT: int = 10
    MIN_MATCH_SCORE: int = 75
    PLAYWRIGHT_HEADLESS: bool = False
    NOTIFICATION_WEBHOOK_URL: Optional[str] = None
    
    # Location Tier Defaults
    LOCATION_TIER_1: list[str] = ["Remote", "Work From Home", "Remote India", "Online"]
    LOCATION_TIER_2: list[str] = ["Hybrid", "Hybrid India"]
    LOCATION_TIER_3: list[str] = ["On-site", "Bangalore", "Delhi", "Mumbai", "Hyderabad", "Pune", "Chennai", "Gurgaon", "Noida"]

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
