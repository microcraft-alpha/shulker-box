"""Url filters."""

from dataclasses import dataclass

from fastapi import Query

from shulker_box.domain import types


@dataclass
class ItemFilters:
    """Item API filters."""

    name: str | None = Query(None)
    category: types.ItemCategory | None = Query(None)
