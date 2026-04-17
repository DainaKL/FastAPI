import logging

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.category_repository import CategoryRepository
from src.schemas.category import Category as CategorySchema
from src.core.exceptions.database_exceptions import CategoryNotFoundException
from src.core.exceptions.domain_exceptions import CategoryNotFoundBySlugException

logger = logging.getLogger(__name__)


class GetCategoryBySlugUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, slug: str) -> CategorySchema:
        try:
            with self._database.session() as session:
                category = self._repo.get_by_slug(session=session, slug=slug)
                return CategorySchema.model_validate(category, from_attributes=True)
        except CategoryNotFoundException:
            error = CategoryNotFoundBySlugException(slug=slug)
            logger.error(error.get_detail())
            raise error
