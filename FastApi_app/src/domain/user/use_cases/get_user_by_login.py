import logging

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.schemas.users import User as UserSchema
from src.core.exceptions.database_exceptions import UserNotFoundException
from src.core.exceptions.domain_exceptions import UserNotFoundByLoginException

logger = logging.getLogger(__name__)


class GetUserByLoginUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = UserRepository()

    async def execute(self, login: str) -> UserSchema:
        try:
            with self._database.session() as session:
                user = self._repo.get_by_login(session=session, login=login)
                return UserSchema.model_validate(user, from_attributes=True)
        except UserNotFoundException:
            error = UserNotFoundByLoginException(login=login)
            logger.error(error.get_detail())
            raise error
