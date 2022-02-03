"""Items logic services."""

import uuid
from dataclasses import asdict

from structlog import get_logger

from shulker_box.api.v1.items import filters, schemas
from shulker_box.domain import exceptions, repositories, types_utils

logger = get_logger(__name__)


class ItemService:
    """Service for items business logic."""

    def __init__(self, repository: repositories.Repository) -> None:
        self.repository = repository

    async def create(
        self,
        data_object: schemas.ItemCreateSchema,
    ) -> schemas.ItemOutSchema:
        """Create a new item.

        Args:
            data_object (ItemCreateSchema): input data object.

        Raises:
            AlreadyExistsError: if an item with the same name already exists.

        Returns:
            ItemOutSchema: output data representation.
        """
        logger.info("Creating a new item", item=data_object)
        items = await self.repository.collect(name=data_object.name)
        if items:
            logger.error("Item already exists", item=items[0])
            raise exceptions.AlreadyExistsError(id=items[0].id)
        item = await self.repository.create(data_object)
        logger.info("Created a new item", item=item)
        return item

    async def collect(
        self,
        url_filters: filters.ItemFilters,
    ) -> list[schemas.ItemOutSchema]:
        """Collect items by given filters.

        Args:
            url_filters (ItemFilters): url filters.

        Returns:
            list[ItemOutSchema]: list of output data representations.
        """
        logger.info("Collecting items", filters=url_filters)
        filters_dict = asdict(
            url_filters,
            dict_factory=types_utils.dict_factory,
        )
        items = await self.repository.collect(**filters_dict)
        logger.info("Collected items", items=items)
        return items

    async def get(self, pk: uuid.UUID) -> schemas.ItemOutSchema:
        """Get an item by its id.

        Args:
            pk (UUID): item id.

        Returns:
            ItemOutSchema: output data representation.
        """
        logger.info("Getting an item", id=pk)
        item = await self.repository.get_by_id(pk)
        logger.info("Got an item", item=item)
        return item

    async def delete(self, pk: uuid.UUID) -> None:
        """Delete an item.

        Args:
            pk (UUID): item id.
        """
        logger.info("Deleting an item", id=pk)
        await self.repository.delete(pk)
        logger.info("Deleted an item", id=pk)

    async def update(
        self,
        pk: uuid.UUID,
        data_object: schemas.ItemUpdateSchema,
    ) -> schemas.ItemOutSchema:
        """Update an existing item.

        Args:
            pk (UUID): item id.
            data_object (ItemUpdateSchema): input data object.

        Raises:
            AlreadyExistsError: if an item with the same name already exists.

        Returns:
            ItemOutSchema: output data representation.
        """
        logger.info("Updating an item", id=pk, item=data_object)
        items = await self.repository.collect(name=data_object.name)
        if items:
            logger.error("Item already exists", item=items[0])
            raise exceptions.AlreadyExistsError(id=items[0].id)
        item = await self.repository.update(pk, data_object)
        logger.info("Updated an item", item=item)
        return item
