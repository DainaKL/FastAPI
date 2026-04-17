import logging

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.location_repository import LocationRepository
from src.schemas.location import Location as LocationSchema
from src.core.exceptions.database_exceptions import DatabaseOperationException

logger = logging.getLogger(__name__)


class GetPublishedLocationsUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, skip: int = 0, limit: int = 100):
        try:
            with self._database.session() as session:
                locations = self._repo.get_published(session=session, skip=skip, limit=limit)
                return [LocationSchema.model_validate(l, from_attributes=True) for l in locations]
        except DatabaseOperationException as e:
            logger.error(e.get_detail())
            raise
