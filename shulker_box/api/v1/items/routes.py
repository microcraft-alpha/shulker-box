"""Items API routes."""


import uuid

from fastapi import APIRouter, Depends
from starlette import status

from shulker_box.api.v1.items import filters, schemas
from shulker_box.domain.items import repositories, services

router = APIRouter(prefix="/items", tags=["items"])

items_service = services.ItemService(repositories.ItemMongoRepository())


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ItemOutSchema,
)
async def create_item(body: schemas.ItemCreateSchema) -> schemas.ItemOutSchema:
    """Create a new item.

    Args:
        body (ItemCreateSchema): item data.

    Returns:
        ItemOutSchema: created item.
    """
    return await items_service.create(body)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.ItemOutSchema],
)
async def get_items(
    url_filters: filters.ItemFilters = Depends(),
) -> list[schemas.ItemOutSchema]:
    """Get all the items.

    Args:
        url_filters (ItemFilters): url params.

    Returns:
        list[ItemOutSchema]: list of items.
    """
    return await items_service.collect(url_filters)


@router.get(
    "/{pk}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ItemOutSchema,
)
async def get_item(pk: uuid.UUID) -> schemas.ItemOutSchema:
    """Get an item by its id.

    Args:
        pk (UUID): item id.

    Returns:
        ItemOutSchema: retrieved item.
    """
    return await items_service.get(pk)


@router.delete(
    "/{pk}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_item(pk: uuid.UUID) -> None:
    """Delete an item.

    Args:
        pk (UUID): item id.
    """
    await items_service.delete(pk)


@router.patch(
    "/{pk}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ItemOutSchema,
)
async def update_item(
    pk: uuid.UUID,
    body: schemas.ItemUpdateSchema,
) -> schemas.ItemOutSchema:
    """Update an existing item.

    Args:
        pk (UUID): item id.
        body (ItemUpdateSchema): update data.

    Returns:
        ItemOutSchema: updated item.
    """
    return await items_service.update(pk, body)
