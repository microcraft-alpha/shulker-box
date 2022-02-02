"""Database utils."""

from beanie import init_beanie
from motor import motor_asyncio

from shulker_box.database.models import Item
from shulker_box.settings import settings


async def init_database():
    """Initialize the database."""
    client = motor_asyncio.AsyncIOMotorClient(settings.DATABASE_URL)
    await init_beanie(
        database=client.db_name,
        document_models=[Item],
    )
