from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlite.models.location import Location
from src.infrastructure.sqlite.repositories.base import BaseRepository


class LocationRepository(BaseRepository[Location]):
    def __init__(self, session: AsyncSession):
        super().__init__(Location, session)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Location]:
        return await super().get_all(skip, limit)

    async def get_by_id(self, location_id: int) -> Optional[Location]:
        return await super().get_by_id(location_id)

    async def get_by_name(self, name: str) -> Optional[Location]:
        result = await self.session.execute(
            select(self.model).where(self.model.name == name)
        )
        return result.scalar_one_or_none()

    async def get_published(self, skip: int = 0, limit: int = 100) -> List[Location]:
        stmt = (
            select(self.model)
            .where(self.model.is_published == True)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create_location(self, **kwargs) -> Location:
        return await self.create(**kwargs)

    async def update_location(self, location_id: int, **kwargs) -> Optional[Location]:
        return await self.update(location_id, **kwargs)

    async def delete_location(self, location_id: int) -> bool:
        return await self.delete(location_id)
