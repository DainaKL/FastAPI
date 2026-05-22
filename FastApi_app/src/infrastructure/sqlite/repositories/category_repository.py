from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlite.models.category import Category as CategoryModel
from src.infrastructure.sqlite.repositories.base import BaseRepository


class CategoryRepository(BaseRepository[CategoryModel]):
    def __init__(self):
        super().__init__(CategoryModel)

    async def get_by_slug(
        self, session: AsyncSession, slug: str
    ) -> Optional[CategoryModel]:
        if not slug:
            return None
        stmt = select(self.model).where(self.model.slug == slug)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
