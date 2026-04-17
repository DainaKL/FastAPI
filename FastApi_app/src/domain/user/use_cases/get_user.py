import logging

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.schemas.users import User as UserSchema
from src.core.exceptions.database_exceptions import UserNotFoundException
from src.core.exceptions.domain_exceptions import UserNotFoundByLoginException

logger = logging.getLogger(__name__)


class GetUserUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> UserSchema:
        try:
            with self._database.session() as session:
                user = self._repo.get_by_id(session=session, user_id=user_id)
                return UserSchema.model_validate(user, from_attributes=True)
        except UserNotFoundException:
            error = UserNotFoundByLoginException(login=str(user_id))
            logger.error(error.get_detail())
            raise error
