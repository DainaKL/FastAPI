import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.location_repository import LocationRepository
from src.schemas.location import Location as LocationSchema, LocationUpdate
from src.core.exceptions.api_exceptions import LocationNotFoundException

logger = logging.getLogger(__name__)


class UpdateLocationUseCase:
    def __init__(self) -> None:
        self._repo = LocationRepository()

    async def execute(self, db: AsyncSession, location_id: int, data: LocationUpdate) -> LocationSchema:
        location = await self._repo.get_by_id(db, location_id)
        if not location:
            raise LocationNotFoundException(location_id=location_id)

        update_dict = {k: v for k, v in data.model_dump().items() if v is not None}
        if not update_dict:
            return LocationSchema.model_validate(location)

        updated = await self._repo.update(db, location_id, **update_dict)
        await db.flush()
        return LocationSchema.model_validate(updated)
