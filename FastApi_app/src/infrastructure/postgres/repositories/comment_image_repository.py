from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from src.infrastructure.postgres.models.comment_image import CommentImage
from src.infrastructure.postgres.repositories.base import BaseRepository

logger = logging.getLogger(__name__)


class CommentImageRepository(BaseRepository[CommentImage]):
    def __init__(self, session: AsyncSession):
        super().__init__(CommentImage, session)

    async def get_by_comment_id(self, comment_id: int) -> List[CommentImage]:
        try:
            stmt = select(self.model).where(self.model.comment_id == comment_id)
            result = await self.session.execute(stmt)
            return list(result.scalars().all())
        except Exception as e:
            logger.error(f"Error getting images for comment {comment_id}: {e}")
            return []

    async def add(self, comment_id: int, url: str) -> Optional[CommentImage]:
        try:
            return await self.create(comment_id=comment_id, url=url)
        except Exception as e:
            logger.error(f"Error adding image for comment {comment_id}: {e}")
            return None

    async def delete_by_id(self, image_id: int) -> bool:
        try:
            image = await self.get_by_id(image_id)
            if not image:
                logger.warning(f"Image with id {image_id} not found")
                return False

            return await self.delete(image_id)
        except Exception as e:
            logger.error(f"Error deleting image {image_id}: {e}")
            return False
