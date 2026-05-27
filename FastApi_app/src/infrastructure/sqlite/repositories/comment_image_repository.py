from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.models.comment_image import CommentImage
from src.infrastructure.sqlite.repositories.base import BaseRepository


class CommentImageRepository(BaseRepository[CommentImage]):
    def __init__(self):
        super().__init__(CommentImage)

    async def add(self, session: AsyncSession, comment_id: int, url: str) -> CommentImage:
        return await self.create(session, comment_id=comment_id, url=url)
