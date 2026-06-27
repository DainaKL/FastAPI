from typing import List, Optional
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from src.infrastructure.postgres.models.comment import Comment
from src.infrastructure.postgres.models.comment_image import CommentImage
from src.infrastructure.postgres.repositories.base import BaseRepository
from src.core.exceptions.api_exceptions import CommentNotFoundException

logger = logging.getLogger(__name__)


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

    async def create(self, **kwargs) -> Comment:
        comment = Comment(**kwargs)
        self.session.add(comment)
        await self.session.flush()
        return comment

    async def update(self, comment_id: int, **kwargs) -> Optional[Comment]:
        comment = await self.get_by_id(comment_id)
        if comment:
            for key, value in kwargs.items():
                if value is not None:
                    setattr(comment, key, value)
            await self.session.flush()
        return comment

    async def delete(self, comment_id: int) -> bool:
        comment = await self.get_by_id(comment_id)
        if comment:
            await self.session.delete(comment)
            await self.session.flush()
            return True
        return False

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
        try:
            image = await self.get_image_by_id(image_id)
            if not image:
                logger.warning(f"Image with id {image_id} not found")
                return False
            await self.session.delete(image)
            await self.session.flush()
            return True
        except Exception as e:
            logger.error(f"Error deleting image {image_id}: {e}")
            return False
