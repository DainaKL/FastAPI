from src.core.logger import logger

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.category_repository import (
    CategoryRepository,
)
from src.schemas.category import Category as CategorySchema
from src.core.exceptions.database_exceptions import DatabaseOperationException
from src.core.exceptions.domain_exceptions import CategoryNotFoundBySlugException


class GetCategoryBySlugUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, slug: str) -> CategorySchema:
        try:
            with self._database.session() as session:
                category = self._repo.get_by_slug(session=session, slug=slug)
                if not category:
                    raise CategoryNotFoundBySlugException(slug=slug)
                return CategorySchema.model_validate(category, from_attributes=True)
        except CategoryNotFoundBySlugException as e:
            raise e
        except DatabaseOperationException as e:
            logger.error(e.get_detail())
            raise
