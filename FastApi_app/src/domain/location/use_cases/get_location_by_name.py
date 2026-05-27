import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.location_repository import LocationRepository
from src.schemas.location import Location as LocationSchema
from src.core.exceptions.api_exceptions import LocationNotFoundException

logger = logging.getLogger(__name__)


class GetLocationByNameUseCase:
    def __init__(self) -> None:
        self._repo = LocationRepository()

    async def execute(self, db: AsyncSession, name: str) -> LocationSchema:
        location = await self._repo.get_by_name(db, name)
        if not location:
            raise LocationNotFoundException(name=name)
        return LocationSchema.model_validate(location)
