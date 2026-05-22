import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.category_repository import (
    CategoryRepository,
)
from src.core.exceptions.database_exceptions import DatabaseOperationException
from src.core.exceptions.domain_exceptions import CategoryNotFoundException

logger = logging.getLogger(__name__)


class DeleteCategoryUseCase:
    def __init__(self) -> None:
        self._repo = CategoryRepository()

    async def execute(self, db: AsyncSession, category_id: int) -> None:
        category = await self._repo.get_by_id(db, category_id)
        if not category:
            raise CategoryNotFoundException(category_id=category_id)

        try:
            await self._repo.delete(db, category_id)
            await db.flush()
        except Exception as e:
            raise DatabaseOperationException("delete", str(e))
