import hashlib
import logging
from src.core.database import get_async_session
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.schemas.users import User as UserSchema, UserUpdate
from src.core.exceptions.domain_exceptions import UserNotFoundByLoginException

logger = logging.getLogger(__name__)


class UpdateUserUseCase:
    def __init__(self) -> None:
        self._repo = UserRepository()

    async def execute(self, user_id: int, data: UserUpdate) -> UserSchema:
        async for session in get_async_session():
            update_dict = {}
            if data.login:
                update_dict["login"] = data.login
            if data.password:
                update_dict["password"] = data.password
            user = await self._repo.update(session=session, user_id=user_id, **update_dict)
            if not user:
                raise UserNotFoundByLoginException(login=str(user_id))
            return UserSchema.model_validate(user, from_attributes=True)