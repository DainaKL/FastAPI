import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.infrastructure.postgres.repositories.location_repository import (
    LocationRepository,
)
from src.schemas.location import Location as LocationSchema
from src.core.exceptions.api_exceptions import (
    InvalidLimitException,
    InvalidSkipException,
)

logger = logging.getLogger(__name__)


class GetLocationsUseCase:
    async def execute(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        if skip < 0:
            raise InvalidSkipException(skip)
        if limit < 1 or limit > 100:
            raise InvalidLimitException(limit)

        repo = LocationRepository(db)
        stmt = select(repo.model).offset(skip).limit(limit)
        result = await db.execute(stmt)
        locations = result.scalars().all()
        return [LocationSchema.model_validate(l) for l in locations]
