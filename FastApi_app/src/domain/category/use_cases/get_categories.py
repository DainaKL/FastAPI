import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.infrastructure.postgres.repositories.category_repository import (
    CategoryRepository,
)
from src.schemas.category import Category as CategorySchema
from src.core.exceptions.api_exceptions import (
    InvalidLimitException,
    InvalidSkipException,
)

logger = logging.getLogger(__name__)


class GetCategoriesUseCase:
    async def execute(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        if skip < 0:
            raise InvalidSkipException(skip)
        if limit < 1 or limit > 100:
            raise InvalidLimitException(limit)

        repo = CategoryRepository(db)
        stmt = select(repo.model).offset(skip).limit(limit)
        result = await db.execute(stmt)
        categories = result.scalars().all()
        return [CategorySchema.model_validate(c) for c in categories]
