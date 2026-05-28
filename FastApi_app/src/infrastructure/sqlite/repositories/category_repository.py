from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlite.models.category import Category
from src.infrastructure.sqlite.repositories.base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, session: AsyncSession):
        super().__init__(Category, session)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Category]:
        return await super().get_all(skip, limit)

    async def get_by_id(self, category_id: int) -> Optional[Category]:
        return await super().get_by_id(category_id)

    async def get_by_slug(self, slug: str) -> Optional[Category]:
        result = await self.session.execute(
            select(self.model).where(self.model.slug == slug)
        )
        return result.scalar_one_or_none()

    async def create_category(self, **kwargs) -> Category:
        return await self.create(**kwargs)

    async def update_category(self, category_id: int, **kwargs) -> Optional[Category]:
        return await self.update(category_id, **kwargs)

    async def delete_category(self, category_id: int) -> bool:
        return await self.delete(category_id)
