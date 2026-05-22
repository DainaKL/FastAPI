import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.category_repository import (
    CategoryRepository,
)
from src.schemas.category import Category as CategorySchema, CategoryUpdate
from src.core.exceptions.database_exceptions import DatabaseOperationException
from src.core.exceptions.domain_exceptions import CategoryNotFoundException

logger = logging.getLogger(__name__)


class UpdateCategoryUseCase:
    def __init__(self) -> None:
        self._repo = CategoryRepository()

    async def execute(
        self, db: AsyncSession, category_id: int, data: CategoryUpdate
    ) -> CategorySchema:
        category = await self._repo.get_by_id(db, category_id)
        if not category:
            raise CategoryNotFoundException(category_id=category_id)

        update_dict = {k: v for k, v in data.model_dump().items() if v is not None}
        if not update_dict:
            return CategorySchema.model_validate(category)

        try:
            updated = await self._repo.update(db, category_id, **update_dict)
            await db.flush()
            return CategorySchema.model_validate(updated)
        except Exception as e:
            raise DatabaseOperationException("update", str(e))
