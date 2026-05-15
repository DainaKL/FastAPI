from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.schemas.users import User as UserSchema
from src.core.database import SessionLocal
from src.core.exceptions.domain_exceptions import UserLoginIsNotUniqueException


class CreateUserUseCase:
    def __init__(self):
        self._repo = UserRepository()

    def execute(self, login: str, password: str) -> UserSchema:
        db = SessionLocal()
        try:
            if self._repo.exists_by_login(db, login):
                raise UserLoginIsNotUniqueException(login=login)

            user = self._repo.create(db, login=login, password=password)
            db.commit()

            return UserSchema.model_validate(user, from_attributes=True)
        finally:
            db.close()
