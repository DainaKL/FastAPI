import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.category_repository import CategoryRepository
from src.schemas.category import Category as CategorySchema, CategoryCreate
from src.core.exceptions.api_exceptions import CategorySlugAlreadyExistsException

logger = logging.getLogger(__name__)


class CreateCategoryUseCase:
    def __init__(self) -> None:
        self._repo = CategoryRepository()

    async def execute(self, db: AsyncSession, data: CategoryCreate) -> CategorySchema:
        existing = await self._repo.get_by_slug(db, slug=data.slug)
        if existing:
            raise CategorySlugAlreadyExistsException(slug=data.slug)

        category = await self._repo.create(db, **data.model_dump())
        await db.flush()
        return CategorySchema.model_validate(category)
