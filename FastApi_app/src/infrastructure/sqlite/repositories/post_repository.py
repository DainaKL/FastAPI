from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlite.models.post import Post as PostModel
from src.infrastructure.sqlite.repositories.base import BaseRepository


class PostRepository(BaseRepository[PostModel]):
    def __init__(self):
        super().__init__(PostModel)

    async def get_by_id(
        self, session: AsyncSession, post_id: int
    ) -> Optional[PostModel]:
        if post_id <= 0:
            return None
        return await super().get_by_id(session, post_id)

    async def get_all(
        self, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[PostModel]:
        return await super().get_all(session, skip, limit)
