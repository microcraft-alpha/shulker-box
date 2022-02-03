"""Items storage classes."""

from shulker_box.api.v1.items import schemas
from shulker_box.database import models
from shulker_box.domain.database import repositories


class ItemMongoRepository(
    repositories.MongoRepository[
        models.Item,
        schemas.ItemCreateSchema,
        schemas.ItemUpdateSchema,
        schemas.ItemOutSchema,
    ],
):
    """Item database storage."""

    table = models.Item
    schema = schemas.ItemOutSchema
