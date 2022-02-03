"""Items API E2E test cases."""

import uuid

import pytest
from fastapi import status
from httpx import AsyncClient

from shulker_box.domain.types import ItemCategory

pytestmark = pytest.mark.asyncio


async def test_item_create(async_client: AsyncClient):
    """Test item creation."""
    response = await async_client.post(
        "/api/v1/items/",
        json={"name": "Sword", "category": ItemCategory.WEAPON},
    )
    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert data["id"] is not None
    assert data["name"] == "Sword"
    assert data["category"] == ItemCategory.WEAPON


async def test_item_create_already_exists(async_client: AsyncClient):
    """Test creating an item with a name that already exists."""
    sword = await async_client.post(
        "/api/v1/items/",
        json={"name": "Sword", "category": ItemCategory.WEAPON},
    )
    response = await async_client.post(
        "/api/v1/items/",
        json={"name": "Sword", "category": ItemCategory.WEAPON},
    )
    data = response.json()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert data["detail"] == f"Object already exists - {sword.json()['id']}"


async def test_item_list(async_client: AsyncClient):
    """Test listing all items."""
    for i in range(3):
        await async_client.post(
            "/api/v1/items/",
            json={"name": f"Block {i}", "category": ItemCategory.BLOCK},
        )
    response = await async_client.get("/api/v1/items/")
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 3


async def test_item_get(async_client: AsyncClient):
    """Test getting an item."""
    sword = await async_client.post(
        "/api/v1/items/",
        json={"name": "Sword", "category": ItemCategory.WEAPON},
    )
    response = await async_client.get(f"/api/v1/items/{sword.json()['id']}")
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data["id"] == sword.json()["id"]
    assert data["name"] == "Sword"
    assert data["category"] == ItemCategory.WEAPON


async def test_item_get_not_found(async_client: AsyncClient):
    """Test getting an item that does not exist."""
    item_id = uuid.uuid4()
    response = await async_client.get(f"/api/v1/items/{item_id}")
    data = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data["detail"] == f"Object does not exist - {item_id}"


async def test_item_delete(async_client: AsyncClient):
    """Test deleting an item."""
    sword = await async_client.post(
        "/api/v1/items/",
        json={"name": "Sword", "category": ItemCategory.WEAPON},
    )
    response = await async_client.delete(f"/api/v1/items/{sword.json()['id']}")
    data = response.json()

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert data is None

    response = await async_client.get("/api/v1/items/")
    data = response.json()

    assert len(data) == 0


async def test_item_delete_not_found(async_client: AsyncClient):
    """Test deleting an item that does not exist."""
    item_id = uuid.uuid4()
    response = await async_client.delete(f"/api/v1/items/{item_id}")
    data = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data["detail"] == f"Object does not exist - {item_id}"


async def test_item_update(async_client: AsyncClient):
    """Test updating an item."""
    sword = await async_client.post(
        "/api/v1/items/",
        json={"name": "Sword", "category": ItemCategory.WEAPON},
    )
    response = await async_client.patch(
        f"/api/v1/items/{sword.json()['id']}",
        json={"name": "Sword of the Ancients"},
    )
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data["id"] == sword.json()["id"]
    assert data["name"] == "Sword of the Ancients"


async def test_item_update_not_found(async_client: AsyncClient):
    """Test updating an item that does not exist."""
    item_id = uuid.uuid4()
    response = await async_client.patch(
        f"/api/v1/items/{item_id}",
        json={"name": "Sword of the Ancients"},
    )
    data = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data["detail"] == f"Object does not exist - {item_id}"


async def test_item_update_not_unique_name(async_client: AsyncClient):
    """Test updating an item with a name that already exists."""
    sword = await async_client.post(
        "/api/v1/items/",
        json={"name": "Sword", "category": ItemCategory.WEAPON},
    )
    another_sword = await async_client.post(
        "/api/v1/items/",
        json={"name": "Sword of the Ancients", "category": ItemCategory.WEAPON},
    )

    response = await async_client.patch(
        f"/api/v1/items/{sword.json()['id']}",
        json={"name": "Sword of the Ancients"},
    )
    data = response.json()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        data["detail"]
        == f"Object already exists - {another_sword.json()['id']}"
    )


async def test_item_update_only_category(async_client: AsyncClient):
    """Test updating an item with only the category field."""
    sword = await async_client.post(
        "/api/v1/items/",
        json={"name": "Sword", "category": ItemCategory.WEAPON},
    )
    response = await async_client.patch(
        f"/api/v1/items/{sword.json()['id']}",
        json={"category": ItemCategory.TOOL},
    )
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data["id"] == sword.json()["id"]
    assert data["category"] == ItemCategory.TOOL
