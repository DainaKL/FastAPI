import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.location_repository import (
    LocationRepository,
)
from src.schemas.location import Location as LocationSchema, LocationCreate
from src.core.exceptions.database_exceptions import DatabaseOperationException
from src.core.exceptions.domain_exceptions import LocationAlreadyExistsException

logger = logging.getLogger(__name__)


class CreateLocationUseCase:
    def __init__(self) -> None:
        self._repo = LocationRepository()

    async def execute(self, db: AsyncSession, data: LocationCreate) -> LocationSchema:
        existing = await self._repo.get_by_name(db, data.name)
        if existing:
            raise LocationAlreadyExistsException(name=data.name)

        try:
            location = await self._repo.create(db, **data.model_dump())
            await db.flush()
            return LocationSchema.model_validate(location)
        except Exception as e:
            raise DatabaseOperationException("create", str(e))
