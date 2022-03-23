"""App settings."""

from environs import Env
from pydantic import BaseSettings

env = Env()


class Settings(BaseSettings):
    """Basic settings for the application."""

    # Application
    TITLE: str = "Shulker Box"
    VERSION: str = "0.0.1"
    DESCRIPTION: str = "API handling Minecraft items"
    DEBUG: bool = env.bool("DEBUG", default=False)

    # Database
    DATABASE_URL: str = env.str("DATABASE_URL")

    # Redis
    REDIS_HOST: str = env.str("REDIS_HOST")
    REDIS_PORT: int = env.int("REDIS_PORT")


settings = Settings()
