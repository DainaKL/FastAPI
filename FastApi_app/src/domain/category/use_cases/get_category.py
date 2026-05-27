import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.category_repository import CategoryRepository
from src.schemas.category import Category as CategorySchema
from src.core.exceptions.api_exceptions import CategoryNotFoundException

logger = logging.getLogger(__name__)


class GetCategoryUseCase:
    def __init__(self) -> None:
        self._repo = CategoryRepository()

    async def execute(self, db: AsyncSession, category_id: int) -> CategorySchema:
        category = await self._repo.get_by_id(db, category_id)
        if not category:
            raise CategoryNotFoundException(category_id=category_id)
        return CategorySchema.model_validate(category)
