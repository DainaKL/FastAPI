import logging

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.location_repository import LocationRepository
from src.schemas.location import Location as LocationSchema
from src.core.exceptions.domain_exceptions import LocationNotFoundByNameException

logger = logging.getLogger(__name__)


class GetLocationByNameUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, name: str) -> LocationSchema:
        try:
            with self._database.session() as session:
                location = self._repo.get_by_name(session=session, name=name)
                if not location:
                    error = LocationNotFoundByNameException(name=name)
                    logger.error(error.get_detail())
                    raise error
                return LocationSchema.model_validate(location, from_attributes=True)
        except LocationNotFoundByNameException as e:
            raise e
        except DatabaseOperationException as e:
            logger.error(e.get_detail())
            raise
