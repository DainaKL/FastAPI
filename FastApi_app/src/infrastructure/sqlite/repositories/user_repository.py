from typing import Type

from sqlalchemy import insert, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.infrastructure.sqlite.models.users import User as UserModel
from src.schemas.users import UserCreate as UserSchema
from src.core.exceptions.database_exceptions import UserNotFoundException, UserAlreadyExistsException


class UserRepository:
    def __init__(self):
        self._model: Type[UserModel] = UserModel

    def get_by_id(self, session: Session, user_id: int) -> UserModel:
        query = select(self._model).where(self._model.id == user_id)
        user = session.scalar(query)
        if not user:
            raise UserNotFoundException(user_id=user_id)
        return user

    def get_by_login(self, session: Session, login: str) -> UserModel:
        query = select(self._model).where(self._model.login == login)
        user = session.scalar(query)
        if not user:
            raise UserNotFoundException(login=login)
        return user

    def get_all(self, session: Session, skip: int = 0, limit: int = 100):
        query = select(self._model).offset(skip).limit(limit)
        return list(session.scalars(query).all())

    def create(self, session: Session, user: UserSchema) -> UserModel:
        query = insert(self._model).values(user.model_dump()).returning(self._model)
        try:
            return session.scalar(query)
        except IntegrityError:
            raise UserAlreadyExistsException(login=user.login)

    def update(self, session: Session, user_id: int, **kwargs) -> UserModel:
        user = self.get_by_id(session, user_id)
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        session.flush()
        session.refresh(user)
        return user

    def delete(self, session: Session, user_id: int) -> None:
        user = self.get_by_id(session, user_id)
        session.delete(user)
        session.flush()
