from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlite.models.category import Category
from src.infrastructure.sqlite.repositories.base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    def __init__(self):
        super().__init__(Category)

    async def get_by_slug(
        self, session: AsyncSession, slug: str
    ) -> Optional[Category]:
        if not slug:
            return None
        stmt = select(self.model).where(self.model.slug == slug)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_published(
        self, session: AsyncSession, skip: int = 0, limit: int = 100
    ):
        stmt = select(self.model).where(self.model.is_published == True).offset(skip).limit(limit)
        result = await session.execute(stmt)
        return list(result.scalars().all())