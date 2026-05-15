from sqlalchemy.orm import Session
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.core.security import verify_password
from src.core.exceptions.domain_exceptions import UserNotFoundByLoginException
from src.core.exceptions.auth_exceptions import InvalidPasswordException


class AuthenticateUserUseCase:
    def execute(self, db: Session, login: str, password: str):
        repo = UserRepository()
        user = repo.get_by_login(db, login)
        if not user:
            raise UserNotFoundByLoginException(login=login)

        if not verify_password(password, user.password):
            raise InvalidPasswordException()

        return user
