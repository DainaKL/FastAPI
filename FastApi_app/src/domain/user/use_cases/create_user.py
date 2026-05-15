import hashlib
import logging
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.schemas.users import User as UserSchema, UserCreate
from src.core.exceptions.domain_exceptions import UserLoginIsNotUniqueException
from src.core.database import SessionLocal

logger = logging.getLogger(__name__)


class CreateUserUseCase:
    def __init__(self) -> None:
        self._repo = UserRepository()

    async def execute(self, data: UserCreate) -> UserSchema:
        db = SessionLocal()
        try:
            existing = self._repo.get_by_login(db, data.login)
            if existing:
                raise UserLoginIsNotUniqueException(login=data.login)

            hashed_password = hashlib.sha256(data.password.encode()).hexdigest()
            user = self._repo.create(db, login=data.login, password=hashed_password)
            return UserSchema.model_validate(user, from_attributes=True)
        finally:
            db.close()