import logging
from src.core.database import get_async_session
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.schemas.users import User as UserSchema

logger = logging.getLogger(__name__)


class GetUsersUseCase:
    def __init__(self) -> None:
        self._repo = UserRepository()

    async def execute(self, skip: int = 0, limit: int = 100):
        async for session in get_async_session():
            users = await self._repo.get_all(session=session, skip=skip, limit=limit)
            return [UserSchema.model_validate(u, from_attributes=True) for u in users]