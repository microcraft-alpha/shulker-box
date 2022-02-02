"""Database models."""

import uuid

from beanie import Document, Indexed
from pydantic import Field

from shulker_box.domain.types import ItemCategory


class Item(Document):
    """Item document model."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: Indexed(str, unique=True)  # type: ignore
    category: ItemCategory
