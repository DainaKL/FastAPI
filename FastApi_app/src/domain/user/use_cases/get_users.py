import logging

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.schemas.users import User as UserSchema
from src.core.exceptions.database_exceptions import DatabaseOperationException

logger = logging.getLogger(__name__)


class GetUsersUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = UserRepository()

    async def execute(self, skip: int = 0, limit: int = 100):
        try:
            with self._database.session() as session:
                users = self._repo.get_all(session=session, skip=skip, limit=limit)
                return [
                    UserSchema.model_validate(u, from_attributes=True) for u in users
                ]
        except DatabaseOperationException as e:
            logger.error(e.get_detail())
            raise
