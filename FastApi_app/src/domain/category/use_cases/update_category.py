import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.postgres.repositories.category_repository import (
    CategoryRepository,
)
from src.schemas.category import Category as CategorySchema, CategoryUpdate
from src.core.exceptions.api_exceptions import (
    CategoryNotFoundException,
    CategoryForbiddenException,
    InvalidIDException,
)

logger = logging.getLogger(__name__)


class UpdateCategoryUseCase:
    async def execute(
        self,
        db: AsyncSession,
        category_id: int,
        data: CategoryUpdate,
        current_user_id: int,
        is_admin: bool,
    ):
        if category_id <= 0:
            raise InvalidIDException(category_id)

        repo = CategoryRepository(db)
        category = await repo.get_by_id(category_id)
        if not category:
            raise CategoryNotFoundException(category_id=category_id)

        if not is_admin and category.author_id != current_user_id:
            raise CategoryForbiddenException(action="редактировать")

        update_dict = {k: v for k, v in data.model_dump().items() if v is not None}
        if update_dict:
            await repo.update(category_id, **update_dict)
            await db.commit()

        return CategorySchema.model_validate(category)
