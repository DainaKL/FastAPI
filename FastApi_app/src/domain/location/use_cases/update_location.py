import logging

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.location_repository import LocationRepository
from src.schemas.location import Location as LocationSchema, LocationUpdate
from src.core.exceptions.database_exceptions import DatabaseOperationException
from src.core.exceptions.domain_exceptions import LocationNotFoundException as DomainLocationNotFoundException

logger = logging.getLogger(__name__)


class UpdateLocationUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int, data: LocationUpdate) -> LocationSchema:
        try:
            with self._database.session() as session:
                location = self._repo.get_by_id(session=session, location_id=location_id)
                if not location:
                    error = DomainLocationNotFoundException(location_id=location_id)
                    logger.error(error.get_detail())
                    raise error

                update_dict = {k: v for k, v in data.model_dump().items() if v is not None}
                updated = self._repo.update(session=session, location_id=location_id, **update_dict)
                return LocationSchema.model_validate(updated, from_attributes=True)
        except DomainLocationNotFoundException as e:
            raise e
        except DatabaseOperationException as e:
            logger.error(e.get_detail())
            raise
