from src.core.logger import logger
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.location_repository import (
    LocationRepository,
)
from src.schemas.location import Location as LocationSchema, LocationCreate
from src.core.exceptions.database_exceptions import (
    LocationAlreadyExistsException,
    DatabaseOperationException,
)
from src.core.exceptions.domain_exceptions import (
    LocationAlreadyExistsException as DomainLocationAlreadyExistsException,
)


class CreateLocationUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, data: LocationCreate) -> LocationSchema:
        try:
            with self._database.session() as session:
                existing = self._repo.get_by_name(session=session, name=data.name)
                if existing:
                    error = DomainLocationAlreadyExistsException(name=data.name)
                    logger.error(error.get_detail())
                    raise error

                location = self._repo.create(session=session, location=data)
                return LocationSchema.model_validate(location, from_attributes=True)
        except DomainLocationAlreadyExistsException as e:
            raise e
        except DatabaseOperationException as e:
            logger.error(e.get_detail())
            raise
