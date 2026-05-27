from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlite.models.post import Post
from src.infrastructure.sqlite.repositories.base import BaseRepository


class PostRepository(BaseRepository[Post]):
    def __init__(self):
        super().__init__(Post)

    async def get_by_id(
        self, session: AsyncSession, post_id: int
    ) -> Optional[Post]:
        if post_id <= 0:
            return None
        return await super().get_by_id(session, post_id)

    async def get_all(
        self, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Post]:
        return await super().get_all(session, skip, limit)

    async def get_published(
        self, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Post]:
        stmt = select(self.model).where(self.model.is_published == True).offset(skip).limit(limit)
        result = await session.execute(stmt)
        return list(result.scalars().all())