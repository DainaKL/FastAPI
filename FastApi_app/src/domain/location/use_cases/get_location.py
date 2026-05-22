import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.location_repository import (
    LocationRepository,
)
from src.schemas.location import Location as LocationSchema
from src.core.exceptions.database_exceptions import DatabaseOperationException
from src.core.exceptions.domain_exceptions import LocationNotFoundException

logger = logging.getLogger(__name__)


class GetLocationUseCase:
    def __init__(self) -> None:
        self._repo = LocationRepository()

    async def execute(self, db: AsyncSession, location_id: int) -> LocationSchema:
        try:
            location = await self._repo.get_by_id(db, location_id)
            if not location:
                raise LocationNotFoundException(location_id=location_id)
            return LocationSchema.model_validate(location)
        except LocationNotFoundException as e:
            raise e
        except Exception as e:
            raise DatabaseOperationException("get_by_id", str(e))
