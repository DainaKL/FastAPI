import logging
from src.core.database import get_async_session
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.schemas.users import User as UserSchema, UserCreate
from src.core.exceptions.domain_exceptions import UserLoginIsNotUniqueException

logger = logging.getLogger(__name__)


class CreateUserUseCase:
    def __init__(self) -> None:
        self._repo = UserRepository()

    async def execute(self, data: UserCreate) -> UserSchema:
        async for session in get_async_session():
            if await self._repo.exists_by_login(session, login=data.login):
                raise UserLoginIsNotUniqueException(login=data.login)

            user = await self._repo.create(session, user=data)
            return UserSchema.model_validate(user, from_attributes=True)