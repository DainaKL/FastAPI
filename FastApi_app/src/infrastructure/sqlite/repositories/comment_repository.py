from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlite.models.comment import Comment as CommentModel
from src.infrastructure.sqlite.repositories.base import BaseRepository


class CommentRepository(BaseRepository[CommentModel]):
    def __init__(self):
        super().__init__(CommentModel)

    async def get_published(
        self, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[CommentModel]:
        stmt = (
            select(self.model)
            .where(self.model.is_published == True)
            .offset(skip)
            .limit(limit)
        )
        result = await session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_post(
        self, session: AsyncSession, post_id: int, skip: int = 0, limit: int = 100
    ) -> List[CommentModel]:
        stmt = (
            select(self.model)
            .where(self.model.post_id == post_id)
            .offset(skip)
            .limit(limit)
        )
        result = await session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_author(
        self, session: AsyncSession, author_id: int, skip: int = 0, limit: int = 100
    ) -> List[CommentModel]:
        stmt = (
            select(self.model)
            .where(self.model.author_id == author_id)
            .offset(skip)
            .limit(limit)
        )
        result = await session.execute(stmt)
        return list(result.scalars().all())
