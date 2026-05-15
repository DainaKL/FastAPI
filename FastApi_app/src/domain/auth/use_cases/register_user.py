from sqlalchemy.orm import Session
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.core.exceptions.domain_exceptions import UserLoginIsNotUniqueException


class RegisterUserUseCase:
    def execute(self, db: Session, login: str, password: str):
        repo = UserRepository()

        if repo.exists_by_login(db, login):
            raise UserLoginIsNotUniqueException(login=login)

        user = repo.create(db, login=login, password=password)
        db.commit()

        return user
