"""App settings."""

from environs import Env
from pydantic import BaseSettings

env = Env()


class Settings(BaseSettings):
    """Basic settings for the application."""

    TITLE: str = "Shulker Box"
    VERSION: str = "0.0.1"
    DESCRIPTION: str = "API handling Minecraft items"
    DEBUG: bool = env.bool("DEBUG", default=False)

    DATABASE_URL: str = env.str("DATABASE_URL")


settings = Settings()
