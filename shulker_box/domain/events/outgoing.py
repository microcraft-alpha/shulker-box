"""Domain events going to the outside world."""


import uuid

from structlog import get_logger

from shulker_box.domain.events.event_types import Event
from shulker_box.domain.types import ItemCategory
from shulker_box.events.bus import eventclass
from shulker_box.events.event_types import OutgoingEventType

logger = get_logger(__name__)


@eventclass(OutgoingEventType.ITEM_CREATED)
class ItemCreated(Event):
    """Event handler for item creation."""

    id: uuid.UUID
    name: str
    category: ItemCategory

    async def handle(self) -> None:
        """Publish info about created item."""


@eventclass(OutgoingEventType.ITEM_DELETED)
class ItemDeleted(Event):
    """Event handler for item deletion."""

    id: uuid.UUID

    async def handle(self) -> None:
        """Publish info about deleted item."""
