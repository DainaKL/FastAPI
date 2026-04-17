import hashlib
import logging

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.schemas.users import User as UserSchema, UserCreate
from src.core.exceptions.database_exceptions import DatabaseOperationException
from src.core.exceptions.domain_exceptions import UserLoginIsNotUniqueException

logger = logging.getLogger(__name__)


class CreateUserUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = UserRepository()

    async def execute(self, data: UserCreate) -> UserSchema:
        try:
            with self._database.session() as session:
                existing = self._repo.get_by_login(session=session, login=data.login)
                if existing:
                    error = UserLoginIsNotUniqueException(login=data.login)
                    logger.error(error.get_detail())
                    raise error

                hashed_password = hashlib.sha256(data.password.encode()).hexdigest()
                user = self._repo.create(session=session, login=data.login, password=hashed_password)
                return UserSchema.model_validate(user, from_attributes=True)
        except UserLoginIsNotUniqueException as e:
            raise e
        except DatabaseOperationException as e:
            logger.error(e.get_detail())
            raise
