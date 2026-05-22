import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.category_repository import (
    CategoryRepository,
)
from src.schemas.category import Category as CategorySchema
from src.core.exceptions.database_exceptions import DatabaseOperationException

logger = logging.getLogger(__name__)


class GetCategoriesUseCase:
    def __init__(self) -> None:
        self._repo = CategoryRepository()

    async def execute(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        try:
            categories = await self._repo.get_all(db, skip=skip, limit=limit)
            return [CategorySchema.model_validate(c) for c in categories]
        except Exception as e:
            raise DatabaseOperationException("get_all", str(e))
