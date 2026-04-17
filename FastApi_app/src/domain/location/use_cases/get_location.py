import logging

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.location_repository import LocationRepository
from src.schemas.location import Location as LocationSchema
from src.core.exceptions.database_exceptions import LocationNotFoundException
from src.core.exceptions.domain_exceptions import LocationNotFoundException as DomainLocationNotFoundException

logger = logging.getLogger(__name__)


class GetLocationUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> LocationSchema:
        try:
            with self._database.session() as session:
                location = self._repo.get_by_id(session=session, location_id=location_id)
                return LocationSchema.model_validate(location, from_attributes=True)
        except LocationNotFoundException:
            error = DomainLocationNotFoundException(location_id=location_id)
            logger.error(error.get_detail())
            raise error
