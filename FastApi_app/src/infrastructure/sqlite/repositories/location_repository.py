from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlite.models.location import Location
from src.infrastructure.sqlite.repositories.base import BaseRepository


class LocationRepository(BaseRepository[Location]):
    def __init__(self):
        super().__init__(Location)

    async def get_by_name(
        self, session: AsyncSession, name: str
    ) -> Optional[Location]:
        if not name:
            return None
        stmt = select(self.model).where(self.model.name == name)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_published(
        self, session: AsyncSession, skip: int = 0, limit: int = 100
    ):
        stmt = select(self.model).where(self.model.is_published == True).offset(skip).limit(limit)
        result = await session.execute(stmt)
        return list(result.scalars().all())