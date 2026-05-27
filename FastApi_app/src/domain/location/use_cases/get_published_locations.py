import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.location_repository import LocationRepository
from src.schemas.location import Location as LocationSchema

logger = logging.getLogger(__name__)


class GetPublishedLocationsUseCase:
    def __init__(self) -> None:
        self._repo = LocationRepository()

    async def execute(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        locations = await self._repo.get_published(db, skip=skip, limit=limit)
        return [LocationSchema.model_validate(l) for l in locations]
