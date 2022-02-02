"""Mobs API schemas."""

import uuid

from shulker_box.api import schemas
from shulker_box.domain.types import ItemCategory


class ItemCreateSchema(schemas.Schema):
    """Item create input schema."""

    name: str
    category: ItemCategory


class ItemUpdateSchema(schemas.Schema):
    """Item update input schema."""

    name: str | None
    category: ItemCategory | None


class ItemOutSchema(schemas.Schema):
    """Item output schema."""

    id: uuid.UUID
    name: str
    category: ItemCategory
