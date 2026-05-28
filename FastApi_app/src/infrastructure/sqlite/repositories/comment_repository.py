from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlite.models.comment import Comment
from src.infrastructure.sqlite.models.comment_image import CommentImage
from src.infrastructure.sqlite.repositories.base import BaseRepository
from src.core.exceptions.api_exceptions import CommentNotFoundException


class CommentRepository(BaseRepository[Comment]):
    def __init__(self, session: AsyncSession):
        super().__init__(Comment, session)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Comment]:
        stmt = (
            select(self.model)
            .options(selectinload(self.model.images))
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, comment_id: int) -> Comment:
        stmt = (
            select(self.model)
            .options(selectinload(self.model.images))
            .where(self.model.id == comment_id)
        )
        result = await self.session.execute(stmt)
        comment = result.scalar_one_or_none()
        if not comment:
            raise CommentNotFoundException(comment_id=comment_id)
        return comment

    async def get_by_post(
        self, post_id: int, skip: int = 0, limit: int = 100
    ) -> List[Comment]:
        stmt = (
            select(self.model)
            .options(selectinload(self.model.images))
            .where(self.model.post_id == post_id)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_author(
        self, author_id: int, skip: int = 0, limit: int = 100
    ) -> List[Comment]:
        stmt = (
            select(self.model)
            .options(selectinload(self.model.images))
            .where(self.model.author_id == author_id)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_published(self, skip: int = 0, limit: int = 100) -> List[Comment]:
        stmt = (
            select(self.model)
            .options(selectinload(self.model.images))
            .where(self.model.is_published == True)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create_comment(self, **kwargs) -> Comment:
        return await self.create(**kwargs)

    async def update_comment(self, comment_id: int, **kwargs) -> Optional[Comment]:
        return await self.update(comment_id, **kwargs)

    async def delete_comment(self, comment_id: int) -> bool:
        return await self.delete(comment_id)

    async def add_image(self, comment_id: int, url: str) -> CommentImage:
        image = CommentImage(comment_id=comment_id, url=url)
        self.session.add(image)
        await self.session.flush()
        return image

    async def get_image_by_id(self, image_id: int) -> Optional[CommentImage]:
        result = await self.session.execute(
            select(CommentImage).where(CommentImage.id == image_id)
        )
        return result.scalar_one_or_none()

    async def delete_image(self, image_id: int) -> bool:
        image = await self.get_image_by_id(image_id)
        if image:
            await self.session.delete(image)
            await self.session.flush()
            return True
        return False
