from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlite.models.location import Location as LocationModel
from src.infrastructure.sqlite.repositories.base import BaseRepository


class LocationRepository(BaseRepository[LocationModel]):
    def __init__(self):
        super().__init__(LocationModel)

    async def get_by_name(
        self, session: AsyncSession, name: str
    ) -> Optional[LocationModel]:
        if not name:
            return None
        stmt = select(self.model).where(self.model.name == name)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_published(
        self, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[LocationModel]:
        stmt = (
            select(self.model)
            .where(self.model.is_published == True)
            .offset(skip)
            .limit(limit)
        )
        result = await session.execute(stmt)
        return list(result.scalars().all())
