"""Storage abstractions."""

import typing as T
import uuid

from shulker_box.api import schemas

CreateSchema = T.TypeVar(
    "CreateSchema",
    bound=schemas.Schema,
    contravariant=True,
)
UpdateSchema = T.TypeVar(
    "UpdateSchema",
    bound=schemas.Schema,
    contravariant=True,
)
OutSchema = T.TypeVar("OutSchema", bound=schemas.Schema)


class Repository(
    T.Generic[CreateSchema, UpdateSchema, OutSchema],
    T.Protocol,
):
    """Storage interface."""

    async def create(self, data_object: CreateSchema) -> OutSchema:
        """Create a new entry.

        Args:
            data_object (CreateSchema): input data object.
        """
        ...  # noqa: WPS428

    async def get_by_id(self, entry_id: uuid.UUID) -> OutSchema:
        """Get an entry by its identifier.

        Args:
            entry_id (UUID): entry ID.
        """
        ...  # noqa: WPS428

    async def collect(
        self,
        **filters,
    ) -> list[OutSchema]:
        """Collect all entries and allow filtering.

        Args:
            filters (dict): additional filters to apply.
        """
        ...  # noqa: WPS428

    async def delete(self, entry_id: uuid.UUID) -> None:
        """Delete an entry.

        Args:
            entry_id (UUID): entry ID.
        """
        ...  # noqa: WPS428

    async def update(
        self,
        entry_id: uuid.UUID,
        data_object: UpdateSchema,
    ) -> OutSchema:
        """Update an existing entry.

        Args:
            entry_id (UUID): entry ID.
            data_object (UpdateSchema): input data object.
        """
        ...  # noqa: WPS428
