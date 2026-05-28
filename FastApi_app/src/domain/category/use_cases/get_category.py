import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.infrastructure.sqlite.repositories.category_repository import (
    CategoryRepository,
)
from src.schemas.category import Category as CategorySchema
from src.core.exceptions.api_exceptions import (
    CategoryNotFoundException,
    InvalidIDException,
)

logger = logging.getLogger(__name__)


class GetCategoryUseCase:
    async def execute(self, db: AsyncSession, category_id: int) -> CategorySchema:
        if category_id <= 0:
            raise InvalidIDException(category_id)

        repo = CategoryRepository(db)
        stmt = select(repo.model).where(repo.model.id == category_id)
        result = await db.execute(stmt)
        category = result.scalar_one_or_none()

        if not category:
            raise CategoryNotFoundException(category_id=category_id)
        return CategorySchema.model_validate(category)
