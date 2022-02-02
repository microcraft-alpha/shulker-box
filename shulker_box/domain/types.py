"""Domain types."""

import enum


class ItemCategory(str, enum.Enum):
    """Item categories."""

    BLOCK = "block"
    WEAPON = "weapon"
    ARMOR = "armor"
    PLANT = "plant"
    FOOD = "food"
    TOOL = "tool"
