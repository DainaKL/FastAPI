import logging
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.category_repository import (
    CategoryRepository,
)
from src.schemas.category import Category as CategorySchema, CategoryCreate
from src.core.exceptions.database_exceptions import DatabaseOperationException

logger = logging.getLogger(__name__)


class CreateCategoryUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, data: CategoryCreate) -> CategorySchema:
        try:
            with self._database.session() as session:
                category = self._repo.create(session=session, category=data)
                return CategorySchema.model_validate(category, from_attributes=True)
        except DatabaseOperationException as e:
            logger.error(e.get_detail())
            raise
