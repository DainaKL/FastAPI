import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.postgres.repositories.location_repository import (
    LocationRepository,
)
from src.schemas.location import Location as LocationSchema, LocationUpdate
from src.core.exceptions.api_exceptions import (
    LocationNotFoundException,
    LocationForbiddenException,
    InvalidIDException,
)

logger = logging.getLogger(__name__)


class UpdateLocationUseCase:
    async def execute(
        self,
        db: AsyncSession,
        location_id: int,
        data: LocationUpdate,
        current_user_id: int,
        is_admin: bool,
    ):
        if location_id <= 0:
            raise InvalidIDException(location_id)

        repo = LocationRepository(db)
        location = await repo.get_by_id(location_id)
        if not location:
            raise LocationNotFoundException(location_id=location_id)

        if not is_admin and location.author_id != current_user_id:
            raise LocationForbiddenException(action="редактировать")

        update_dict = {k: v for k, v in data.model_dump().items() if v is not None}
        if update_dict:
            await repo.update(location_id, **update_dict)
            await db.commit()

        return LocationSchema.model_validate(location)
