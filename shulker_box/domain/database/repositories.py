"""Database storage classes."""

import typing as T
import uuid

from beanie import Document
from structlog import get_logger

from shulker_box.domain import exceptions, repositories
from shulker_box.domain.database.queries import create_query

logger = get_logger(__name__)

Model = T.TypeVar("Model", bound=Document)


class MongoRepository(
    T.Generic[
        Model,
        repositories.CreateSchema,
        repositories.UpdateSchema,
        repositories.OutSchema,
    ],
):
    """Generic database storage for ORM models."""

    table: type[Model]
    schema: type[repositories.OutSchema]

    async def create(
        self,
        data_object: repositories.CreateSchema,
    ) -> repositories.OutSchema:
        """Create a new entry.

        Args:
            data_object (CreateSchema): input data object.

        Returns:
            OutSchema: output data representation.
        """
        entry = await self.table(**data_object.dict()).insert()
        return self.schema.from_orm(entry)

    async def collect(
        self,
        **filters,
    ) -> list[repositories.OutSchema]:
        """Collect all entries nased on the query.

        Args:
            filters (dict): filters to apply.

        Returns:
            list[OutSchema]: list of output data representations.
        """
        query = create_query(filters, self.table)
        return [
            self.schema.from_orm(entry)
            async for entry in self.table.find(query)
        ]

    async def get_by_id(self, entry_id: uuid.UUID) -> repositories.OutSchema:
        """Get an entry by its id.

        Args:
            entry_id (UUID): primary key.

        Raises:
            DoesNotExistError: when entry does not exist.

        Returns:
            OutSchema: output data representation.
        """
        entry = await self.table.find_one(self.table.id == entry_id)
        if not entry:
            logger.error("Entry was not found", id=entry_id)
            raise exceptions.DoesNotExistError(id=entry_id)
        return self.schema.from_orm(entry)

    async def delete(self, entry_id: uuid.UUID) -> None:
        """Get an entry by its id and delete it.

        Args:
            entry_id (UUID): primary key.

        Raises:
            DoesNotExistError: when entry does not exist.
        """
        entry = await self.table.find_one(self.table.id == entry_id)
        if not entry:
            logger.error("Entry was not found", id=entry_id)
            raise exceptions.DoesNotExistError(id=entry_id)
        await entry.delete()

    async def update(
        self,
        entry_id: uuid.UUID,
        data_object: repositories.UpdateSchema,
    ) -> repositories.OutSchema:
        """Update an existing entry.

        Args:
            entry_id (UUID): primary key.
            data_object (CreateSchema): input data object.

        Raises:
            DoesNotExistError: when entry does not exist.

        Returns:
            OutSchema: output data representation.
        """
        query = create_query(data_object.dict(exclude_unset=True), self.table)
        update_result = await self.table.find_one(
            self.table.id == entry_id,
        ).set(query)
        if getattr(update_result, "matched_count", 0) == 0:
            logger.error("Entry was not found", id=entry_id)
            raise exceptions.DoesNotExistError(id=entry_id)
        return await self.get_by_id(entry_id)
