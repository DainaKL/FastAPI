import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.infrastructure.postgres.repositories.location_repository import (
    LocationRepository,
)
from src.schemas.location import Location as LocationSchema
from src.core.exceptions.api_exceptions import (
    LocationNotFoundException,
    InvalidIDException,
)

logger = logging.getLogger(__name__)


class GetLocationUseCase:
    async def execute(self, db: AsyncSession, location_id: int) -> LocationSchema:
        if location_id <= 0:
            raise InvalidIDException(location_id)

        repo = LocationRepository(db)
        stmt = select(repo.model).where(repo.model.id == location_id)
        result = await db.execute(stmt)
        location = result.scalar_one_or_none()

        if not location:
            raise LocationNotFoundException(location_id=location_id)
        return LocationSchema.model_validate(location)
