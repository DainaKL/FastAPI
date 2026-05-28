from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlite.models.comment_image import CommentImage
from src.infrastructure.sqlite.repositories.base import BaseRepository


class CommentImageRepository(BaseRepository[CommentImage]):
    def __init__(self, session: AsyncSession):
        super().__init__(CommentImage, session)

    async def get_by_comment_id(self, comment_id: int) -> List[CommentImage]:
        stmt = select(self.model).where(self.model.comment_id == comment_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def add(self, comment_id: int, url: str) -> CommentImage:
        return await self.create(comment_id=comment_id, url=url)
