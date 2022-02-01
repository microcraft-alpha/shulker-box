"""Mobs API schemas."""

import enum
import uuid

from shulker_box.api import schemas


class ItemCategory(enum.Enum):
    """Item categories."""

    BLOCK = "block"
    WEAPON = "weapon"
    ARMOR = "armor"
    PLANT = "plant"
    FOOD = "food"
    TOOL = "tool"


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
