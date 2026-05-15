import logging
from src.core.database import get_async_session
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.schemas.users import User as UserSchema
from src.core.exceptions.domain_exceptions import UserNotFoundByLoginException

logger = logging.getLogger(__name__)


class GetUserByLoginUseCase:
    def __init__(self) -> None:
        self._repo = UserRepository()

    async def execute(self, login: str) -> UserSchema:
        async for session in get_async_session():
            user = await self._repo.get_by_login(session=session, login=login)
            return UserSchema.model_validate(user, from_attributes=True)