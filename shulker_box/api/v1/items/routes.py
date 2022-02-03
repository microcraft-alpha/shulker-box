"""Mob API routes."""


import uuid

from fastapi import APIRouter
from starlette import status

from shulker_box.api.v1.items import schemas
from shulker_box.database.models import Item
from shulker_box.database.queries import create_query
from shulker_box.domain import exceptions

router = APIRouter(prefix="/items", tags=["items"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ItemOutSchema,
)
async def create_item(body: schemas.ItemCreateSchema) -> schemas.ItemOutSchema:
    """Create a new item.

    Args:
        body (ItemCreateSchema): item data.

    Raises:
        AlreadyExistsError: if item already exists.

    Returns:
        ItemOutSchema: created item.
    """
    existing_item = await Item.find_one(Item.name == body.name)
    if existing_item:
        raise exceptions.AlreadyExistsError(id=existing_item.id)
    item = await Item(**body.dict()).insert()
    return schemas.ItemOutSchema(**item.dict())


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.ItemOutSchema],
)
async def get_items() -> list[schemas.ItemOutSchema]:
    """Get all the items.

    Returns:
        list[ItemOutSchema]: list of items.
    """
    return [schemas.ItemOutSchema(**item.dict()) async for item in Item.all()]


@router.get(
    "/{pk}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ItemOutSchema,
)
async def get_item(pk: uuid.UUID) -> schemas.ItemOutSchema:
    """Get an item by its id.

    Args:
        pk (UUID): item id.

    Raises:
        DoesNotExistError: if item does not exist.

    Returns:
        ItemOutSchema: retrieved item.
    """
    item = await Item.find_one(Item.id == pk)
    if not item:
        raise exceptions.DoesNotExistError(id=pk)
    return schemas.ItemOutSchema(**item.dict())


@router.delete(
    "/{pk}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_item(pk: uuid.UUID) -> None:
    """Delete an item.

    Args:
        pk (UUID): item id.

    Raises:
        DoesNotExistError: if item does not exist.
    """
    item = await Item.find_one(Item.id == pk)
    if not item:
        raise exceptions.DoesNotExistError(id=pk)
    await item.delete()


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

    Raises:
        DoesNotExistError: if item does not exist.
        AlreadyExistsError: if item violates unique constraint.

    Returns:
        ItemOutSchema: updated item.
    """
    existing_item = await Item.find_one(Item.name == body.name)
    if existing_item:
        raise exceptions.AlreadyExistsError(id=existing_item.id)

    query = create_query(body.dict(exclude_unset=True), Item)
    result = await Item.find_one(Item.id == pk).set(query)
    if result.matched_count == 0:  # type: ignore
        raise exceptions.DoesNotExistError(id=pk)

    item = await Item.find_one(Item.id == pk)
    return schemas.ItemOutSchema(**item.dict())  # type: ignore
