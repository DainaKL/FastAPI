import logging

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.location_repository import (
    LocationRepository,
)
from src.core.exceptions.database_exceptions import DatabaseOperationException
from src.core.exceptions.domain_exceptions import (
    LocationNotFoundException as DomainLocationNotFoundException,
)

logger = logging.getLogger(__name__)


class DeleteLocationUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> None:
        try:
            with self._database.session() as session:
                location = self._repo.get_by_id(
                    session=session, location_id=location_id
                )
                if not location:
                    error = DomainLocationNotFoundException(location_id=location_id)
                    logger.error(error.get_detail())
                    raise error

                self._repo.delete(session=session, location_id=location_id)
        except DomainLocationNotFoundException as e:
            raise e
        except DatabaseOperationException as e:
            logger.error(e.get_detail())
            raise
