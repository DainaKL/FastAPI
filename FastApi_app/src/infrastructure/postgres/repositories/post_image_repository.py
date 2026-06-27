from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from src.infrastructure.postgres.models.post_image import PostImage
from src.infrastructure.postgres.repositories.base import BaseRepository

logger = logging.getLogger(__name__)


class PostImageRepository(BaseRepository[PostImage]):
    def __init__(self, session: AsyncSession):
        super().__init__(PostImage, session)

    async def get_by_post_id(self, post_id: int) -> List[PostImage]:
        try:
            stmt = select(self.model).where(self.model.post_id == post_id)
            result = await self.session.execute(stmt)
            return list(result.scalars().all())
        except Exception as e:
            logger.error(f"Error getting images for post {post_id}: {e}")
            return []

    async def add(self, post_id: int, url: str) -> Optional[PostImage]:
        try:
            return await self.create(post_id=post_id, url=url)
        except Exception as e:
            logger.error(f"Error adding image for post {post_id}: {e}")
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
