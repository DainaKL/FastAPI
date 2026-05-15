import logging
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.category_repository import (
    CategoryRepository,
)
from src.schemas.category import Category as CategorySchema, CategoryCreate
from src.core.exceptions.database_exceptions import DatabaseOperationException
from src.core.exceptions.domain_exceptions import CategorySlugAlreadyExistsException

logger = logging.getLogger(__name__)


class CreateCategoryUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, data: CategoryCreate) -> CategorySchema:
        try:
            with self._database.session() as session:
                existing = self._repo.get_by_slug(session=session, slug=data.slug)
                if existing:
                    error = CategorySlugAlreadyExistsException(slug=data.slug)
                    logger.error(error.get_detail())
                    raise error

                category = self._repo.create(session=session, category=data)
                return CategorySchema.model_validate(category, from_attributes=True)
        except CategorySlugAlreadyExistsException as e:
            raise e
        except DatabaseOperationException as e:
            logger.error(e.get_detail())
            raise
