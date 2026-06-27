import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.postgres.repositories.category_repository import (
    CategoryRepository,
)
from src.schemas.category import Category as CategorySchema
from src.core.exceptions.api_exceptions import CategoryNotFoundException

logger = logging.getLogger(__name__)


class GetCategoryBySlugUseCase:
    async def execute(self, db: AsyncSession, slug: str) -> CategorySchema:
        repo = CategoryRepository(db)
        category = await repo.get_by_slug(slug)

        if not category:
            raise CategoryNotFoundException(slug=slug)
        return CategorySchema.model_validate(category)
