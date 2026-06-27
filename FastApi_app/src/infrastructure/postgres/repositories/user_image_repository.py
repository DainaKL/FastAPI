from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from src.infrastructure.postgres.models.user_image import UserImage
from src.infrastructure.postgres.repositories.base import BaseRepository

logger = logging.getLogger(__name__)


class UserImageRepository(BaseRepository[UserImage]):
    def __init__(self, session: AsyncSession):
        super().__init__(UserImage, session)

    async def get_by_user_id(self, user_id: int) -> List[UserImage]:
        try:
            stmt = select(self.model).where(self.model.user_id == user_id)
            result = await self.session.execute(stmt)
            return list(result.scalars().all())
        except Exception as e:
            logger.error(f"Error getting images for user {user_id}: {e}")
            return []

    async def add(self, user_id: int, url: str) -> Optional[UserImage]:
        try:
            return await self.create(user_id=user_id, url=url)
        except Exception as e:
            logger.error(f"Error adding image for user {user_id}: {e}")
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

    async def set_profile_image(self, user_id: int, url: str) -> UserImage:
        images = await self.get_by_user_id(user_id)
        for img in images:
            await self.delete(img.id)
        return await self.add(user_id, url)
