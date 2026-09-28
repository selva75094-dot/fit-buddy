from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class Settings(BaseModel):
    app_name: str = Field(default="FitBuddy")
    gemini_api_key: str | None = None
    gemini_workout_model: str = "gemini-2.5-pro"
    gemini_tip_model: str = "gemini-2.5-flash"
    database_url: str = f"sqlite:///{BASE_DIR / 'fitbuddy.db'}"

    @classmethod
    def from_env(cls) -> "Settings":
        import os

        return cls(
            app_name=os.getenv("APP_NAME", "FitBuddy"),
            gemini_api_key=os.getenv("GEMINI_API_KEY"),
            gemini_workout_model=os.getenv("GEMINI_WORKOUT_MODEL", "gemini-2.5-pro"),
            gemini_tip_model=os.getenv("GEMINI_TIP_MODEL", "gemini-2.5-flash"),
            database_url=os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'fitbuddy.db'}"),
        )


@lru_cache
def get_settings() -> Settings:
    return Settings.from_env()
