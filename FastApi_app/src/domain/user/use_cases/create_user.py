import hashlib
import logging
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.schemas.users import User as UserSchema, UserCreate
from src.core.exceptions.domain_exceptions import UserLoginIsNotUniqueException

logger = logging.getLogger(__name__)


class CreateUserUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = UserRepository()

    async def execute(self, data: UserCreate) -> UserSchema:
        with self._database.session() as session:
            if self._repo.exists_by_login(session=session, login=data.login):
                raise UserLoginIsNotUniqueException(login=data.login)

            hashed_password = hashlib.sha256(data.password.encode()).hexdigest()
            user = self._repo.create(session=session, user=data)
            return UserSchema.model_validate(user, from_attributes=True)
