from typing import Type

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.core.exceptions.database_exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
)
from src.infrastructure.sqlite.models.users import User as UserModel
from src.schemas.users import User as UserSchema


class UserRepository:
    def __init__(self):
        self._model: Type[UserModel] = UserModel

    def get(self, session: Session, login: str) -> UserModel:
        query = select(self._model).where(self._model.login == login)

        user = session.scalar(query)
        if not user:
            raise UserNotFoundException()

        return user

    def create(self, session: Session, user: UserSchema) -> UserModel:
        query = insert(self._model).values(user.model_dump()).returning(self._model)

        try:
            user = session.scalar(query)
        except IntegrityError:
            raise UserAlreadyExistsException()

        return user
