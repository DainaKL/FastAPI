import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.postgres.repositories.location_repository import (
    LocationRepository,
)
from src.schemas.location import Location as LocationSchema, LocationCreate
from src.core.exceptions.api_exceptions import LocationAlreadyExistsException

logger = logging.getLogger(__name__)


class CreateLocationUseCase:
    async def execute(self, db: AsyncSession, data: LocationCreate, author_id: int):
        repo = LocationRepository(db)
        existing = await repo.get_by_name(data.name)
        if existing:
            raise LocationAlreadyExistsException(name=data.name)

        location = await repo.create(
            name=data.name, is_published=data.is_published, author_id=author_id
        )
        await db.commit()
        return LocationSchema.model_validate(location)
