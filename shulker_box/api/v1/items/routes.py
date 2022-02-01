"""Mob API routes."""

import uuid

from fastapi import APIRouter
from starlette import status

from shulker_box.api.v1.items import schemas

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

    Returns:
        ItemOutSchema: created item.
    """
    return schemas.ItemOutSchema(
        id=uuid.uuid4(),
        **body.dict(),
    )


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
    return [
        schemas.ItemOutSchema(
            id=uuid.uuid4(),
            name="Test Item",
            category=schemas.ItemCategory.BLOCK,
        ),
    ]


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
    return schemas.ItemOutSchema(
        id=pk,
        name="Test Item",
        category=schemas.ItemCategory.BLOCK,
    )


@router.delete(
    "/{pk}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_item(pk: uuid.UUID) -> None:
    """Delete an item.

    Args:
        pk (UUID): item id.
    """


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
    return schemas.ItemOutSchema(
        id=uuid.uuid4(),
        name="Test Item",
        category=schemas.ItemCategory.BLOCK,
    )
