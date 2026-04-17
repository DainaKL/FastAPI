import logging

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.core.exceptions.database_exceptions import DatabaseOperationException
from src.core.exceptions.domain_exceptions import UserNotFoundByLoginException

logger = logging.getLogger(__name__)


class DeleteUserUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> None:
        try:
            with self._database.session() as session:
                user = self._repo.get_by_id(session=session, user_id=user_id)
                if not user:
                    error = UserNotFoundByLoginException(login=str(user_id))
                    logger.error(error.get_detail())
                    raise error

                self._repo.delete(session=session, user_id=user_id)
        except UserNotFoundByLoginException as e:
            raise e
        except DatabaseOperationException as e:
            logger.error(e.get_detail())
            raise
