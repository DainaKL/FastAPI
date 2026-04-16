import hashlib
from typing import List

from src.core.exceptions.database_exceptions import (
    DatabaseOperationException, UserAlreadyExistsException,
    UserNotFoundException)
from src.core.exceptions.domain_exceptions import (
    UserLoginIsNotUniqueException, UserNotFoundByLoginException)
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.user_repository import \
    UserRepository
from src.schemas.users import User, UserCreate, UserUpdate


class UserUseCases:
    def __init__(self):
        self._database = database

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        with self._database.session() as session:
            repo = UserRepository(session)
            users = repo.get_all(skip=skip, limit=limit)
            return [User.model_validate(u, from_attributes=True) for u in users]

    async def get_by_login(self, login: str) -> User:
        with self._database.session() as session:
            repo = UserRepository(session)
            try:
                user = repo.get_by_login(login)
                return User.model_validate(user, from_attributes=True)
            except UserNotFoundException:
                raise UserNotFoundByLoginException(login=login)
            except DatabaseOperationException:
                raise UserNotFoundByLoginException(login=login)

    async def get_by_id(self, user_id: int) -> User:
        with self._database.session() as session:
            repo = UserRepository(session)
            try:
                user = repo.get_by_id(user_id)
                return User.model_validate(user, from_attributes=True)
            except UserNotFoundException:
                raise UserNotFoundByLoginException(login=str(user_id))
            except DatabaseOperationException:
                raise UserNotFoundByLoginException(login=str(user_id))

    async def create(self, data: UserCreate) -> User:
        with self._database.session() as session:
            repo = UserRepository(session)
            try:
                existing = repo.get_by_login(data.login)
                if existing:
                    raise UserLoginIsNotUniqueException(login=data.login)
            except UserNotFoundException:
                pass

            try:
                hashed_password = hashlib.sha256(data.password.encode()).hexdigest()
                user = repo.create(login=data.login, password=hashed_password)
                return User.model_validate(user, from_attributes=True)
            except UserAlreadyExistsException:
                raise UserLoginIsNotUniqueException(login=data.login)
            except DatabaseOperationException:
                raise UserLoginIsNotUniqueException(login=data.login)

    async def update(self, user_id: int, data: UserUpdate) -> User:
        with self._database.session() as session:
            repo = UserRepository(session)
            try:
                update_dict = {}
                if data.login:
                    update_dict["login"] = data.login
                if data.password:
                    update_dict["password"] = hashlib.sha256(
                        data.password.encode()
                    ).hexdigest()
                user = repo.update(user_id, **update_dict)
                return User.model_validate(user, from_attributes=True)
            except UserNotFoundException:
                raise UserNotFoundByLoginException(login=str(user_id))

    async def delete(self, user_id: int) -> None:
        with self._database.session() as session:
            repo = UserRepository(session)
            try:
                repo.delete(user_id)
            except UserNotFoundException:
                raise UserNotFoundByLoginException(login=str(user_id))
