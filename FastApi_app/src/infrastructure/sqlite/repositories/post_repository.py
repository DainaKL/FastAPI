from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlite.models.post import Post
from src.infrastructure.sqlite.models.post_image import PostImage
from src.infrastructure.sqlite.repositories.base import BaseRepository
from src.core.exceptions.api_exceptions import PostNotFoundException


class PostRepository(BaseRepository[Post]):
    def __init__(self, session: AsyncSession):
        super().__init__(Post, session)

    def _get_base_query(self):
        return select(self.model).options(
            joinedload(self.model.author),
            joinedload(self.model.location),
            joinedload(self.model.category),
            selectinload(self.model.images),
        )

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Post]:
        stmt = self._get_base_query().offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.unique().scalars().all())

    async def get_by_id(self, post_id: int) -> Post:
        stmt = self._get_base_query().where(self.model.id == post_id)
        result = await self.session.execute(stmt)
        post = result.unique().scalar_one_or_none()
        if not post:
            raise PostNotFoundException(post_id=post_id)
        return post

    async def create_post(self, **kwargs) -> Post:
        return await self.create(**kwargs)

    async def update_post(self, post_id: int, **kwargs) -> Optional[Post]:
        return await self.update(post_id, **kwargs)

    async def delete_post(self, post_id: int) -> bool:
        return await self.delete(post_id)

    async def add_image(self, post_id: int, url: str) -> PostImage:
        image = PostImage(post_id=post_id, url=url)
        self.session.add(image)
        await self.session.flush()
        return image

    async def get_image_by_id(self, image_id: int) -> Optional[PostImage]:
        result = await self.session.execute(
            select(PostImage).where(PostImage.id == image_id)
        )
        return result.scalar_one_or_none()

    async def delete_image(self, image_id: int) -> bool:
        image = await self.get_image_by_id(image_id)
        if image:
            await self.session.delete(image)
            await self.session.flush()
            return True
        return False
