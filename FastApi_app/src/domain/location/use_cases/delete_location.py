import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.postgres.repositories.location_repository import (
    LocationRepository,
)
from src.core.exceptions.api_exceptions import (
    LocationNotFoundException,
    LocationForbiddenException,
    InvalidIDException,
)

logger = logging.getLogger(__name__)


class DeleteLocationUseCase:
    async def execute(
        self, db: AsyncSession, location_id: int, current_user_id: int, is_admin: bool
    ):
        if location_id <= 0:
            raise InvalidIDException(location_id)

        repo = LocationRepository(db)
        location = await repo.get_by_id(location_id)
        if not location:
            raise LocationNotFoundException(location_id=location_id)

        if not is_admin and location.author_id != current_user_id:
            raise LocationForbiddenException(action="удалять")

        await repo.delete(location_id)
        await db.commit()
