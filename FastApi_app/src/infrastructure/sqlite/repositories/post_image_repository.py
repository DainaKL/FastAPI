from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlite.models.post_image import PostImage
from src.infrastructure.sqlite.repositories.base import BaseRepository


class PostImageRepository(BaseRepository[PostImage]):
    def __init__(self, session: AsyncSession):
        super().__init__(PostImage, session)

    async def get_by_post_id(self, post_id: int) -> List[PostImage]:
        stmt = select(self.model).where(self.model.post_id == post_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def add(self, post_id: int, url: str) -> PostImage:
        return await self.create(post_id=post_id, url=url)

    async def delete_by_id(self, image_id: int) -> bool:
        return await self.delete(image_id)
