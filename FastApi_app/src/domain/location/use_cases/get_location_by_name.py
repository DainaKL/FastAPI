import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.location_repository import (
    LocationRepository,
)
from src.schemas.location import Location as LocationSchema
from src.core.exceptions.database_exceptions import DatabaseOperationException
from src.core.exceptions.domain_exceptions import LocationNotFoundByNameException

logger = logging.getLogger(__name__)


class GetLocationByNameUseCase:
    def __init__(self) -> None:
        self._repo = LocationRepository()

    async def execute(self, db: AsyncSession, name: str) -> LocationSchema:
        try:
            location = await self._repo.get_by_name(db, name)
            if not location:
                raise LocationNotFoundByNameException(name=name)
            return LocationSchema.model_validate(location)
        except LocationNotFoundByNameException as e:
            raise e
        except Exception as e:
            raise DatabaseOperationException("get_by_name", str(e))
