"""Typing helpers."""

import typing as T

DictItems = list[tuple[str, T.Any]]


def dict_factory(dict_items: DictItems) -> dict[str, T.Any]:
    """Convert a list of tuples into a dictionary.

    Args:
        dict_items (DictItems): list of tuples.

    Returns:
        dict[str, Any]: dictionary without empty values.
    """
    return {key: value for key, value in dict_items if value}
