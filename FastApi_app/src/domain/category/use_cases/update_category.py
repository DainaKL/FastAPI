import logging

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.category_repository import CategoryRepository
from src.schemas.category import Category as CategorySchema, CategoryUpdate
from src.core.exceptions.database_exceptions import DatabaseOperationException
from src.core.exceptions.domain_exceptions import CategoryNotFoundException as DomainCategoryNotFoundException

logger = logging.getLogger(__name__)


class UpdateCategoryUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int, data: CategoryUpdate) -> CategorySchema:
        try:
            with self._database.session() as session:
                category = self._repo.get_by_id(session=session, category_id=category_id)
                if not category:
                    error = DomainCategoryNotFoundException(category_id=category_id)
                    logger.error(error.get_detail())
                    raise error

                update_dict = {k: v for k, v in data.model_dump().items() if v is not None}
                updated = self._repo.update(session=session, category_id=category_id, **update_dict)
                return CategorySchema.model_validate(updated, from_attributes=True)
        except DomainCategoryNotFoundException as e:
            raise e
        except DatabaseOperationException as e:
            logger.error(e.get_detail())
            raise
