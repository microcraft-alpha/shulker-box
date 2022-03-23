"""Service level event types."""

import enum


class EventType(str, enum.Enum):  # noqa: WPS600
    """Event types enum."""


class IncomingEventType(EventType):
    """Incoming event types."""


class OutgoingEventType(EventType):
    """Incoming event types."""

    ITEM_CREATED = "item-created"
    ITEM_DELETED = "item-deleted"
