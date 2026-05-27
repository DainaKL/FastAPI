import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.location_repository import LocationRepository
from src.core.exceptions.api_exceptions import LocationNotFoundException

logger = logging.getLogger(__name__)


class DeleteLocationUseCase:
    def __init__(self) -> None:
        self._repo = LocationRepository()

    async def execute(self, db: AsyncSession, location_id: int) -> None:
        location = await self._repo.get_by_id(db, location_id)
        if not location:
            raise LocationNotFoundException(location_id=location_id)

        await self._repo.delete(db, location_id)
        await db.flush()
