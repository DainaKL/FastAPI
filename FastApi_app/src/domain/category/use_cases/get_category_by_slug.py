import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.category_repository import (
    CategoryRepository,
)
from src.schemas.category import Category as CategorySchema
from src.core.exceptions.database_exceptions import DatabaseOperationException
from src.core.exceptions.domain_exceptions import CategoryNotFoundBySlugException

logger = logging.getLogger(__name__)


class GetCategoryBySlugUseCase:
    def __init__(self) -> None:
        self._repo = CategoryRepository()

    async def execute(self, db: AsyncSession, slug: str) -> CategorySchema:
        try:
            category = await self._repo.get_by_slug(db, slug)
            if not category:
                raise CategoryNotFoundBySlugException(slug=slug)
            return CategorySchema.model_validate(category)
        except CategoryNotFoundBySlugException as e:
            raise e
        except Exception as e:
            raise DatabaseOperationException("get_by_slug", str(e))
