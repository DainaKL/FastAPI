import logging

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.category_repository import (
    CategoryRepository,
)
from src.schemas.category import Category as CategorySchema
from src.core.exceptions.database_exceptions import DatabaseOperationException

logger = logging.getLogger(__name__)


class GetCategoriesUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, skip: int = 0, limit: int = 100):
        try:
            with self._database.session() as session:
                categories = self._repo.get_all(session=session, skip=skip, limit=limit)
                return [
                    CategorySchema.model_validate(c, from_attributes=True)
                    for c in categories
                ]
        except DatabaseOperationException as e:
            logger.error(e.get_detail())
            raise
