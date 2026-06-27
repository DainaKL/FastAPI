import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.postgres.repositories.category_repository import (
    CategoryRepository,
)
from src.schemas.category import Category as CategorySchema, CategoryCreate
from src.core.exceptions.api_exceptions import CategorySlugAlreadyExistsException

logger = logging.getLogger(__name__)


class CreateCategoryUseCase:
    async def execute(self, db: AsyncSession, data: CategoryCreate, author_id: int):
        repo = CategoryRepository(db)
        existing = await repo.get_by_slug(data.slug)
        if existing:
            raise CategorySlugAlreadyExistsException(slug=data.slug)

        category = await repo.create(
            title=data.title,
            description=data.description,
            slug=data.slug,
            is_published=data.is_published,
            author_id=author_id,
        )
        await db.commit()
        return CategorySchema.model_validate(category)
