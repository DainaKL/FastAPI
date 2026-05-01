from typing import Type
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.infrastructure.sqlite.models.users import User as UserModel
from src.schemas.users import UserCreate as UserSchema
from src.core.exceptions.database_exceptions import (
    UserAlreadyExistsException,
    DatabaseOperationException,
)
from src.core.security import get_password_hash


class UserRepository:
    def __init__(self):
        self._model: Type[UserModel] = UserModel

    def get_by_id(self, session: Session, user_id: int):
        if user_id <= 0:
            return None
        query = select(self._model).where(self._model.id == user_id)
        return session.scalar(query)

    def get_by_login(self, session: Session, login: str):
        if not login:
            return None
        query = select(self._model).where(self._model.login == login)
        return session.scalar(query)

    def exists_by_login(self, session: Session, login: str) -> bool:
        if not login:
            return False
        query = select(self._model).where(self._model.login == login)
        return session.scalar(query) is not None

    def get_all(self, session: Session, skip: int = 0, limit: int = 100):
        query = select(self._model).offset(skip).limit(limit)
        return list(session.scalars(query).all())

    def create(self, session: Session, user: UserSchema) -> UserModel:
        try:
            user_dict = user.model_dump()
            user_dict["password"] = get_password_hash(user_dict["password"])
            query = insert(self._model).values(user_dict).returning(self._model)
            return session.scalar(query)
        except IntegrityError:
            raise UserAlreadyExistsException(login=user.login)

    def update(self, session: Session, user_id: int, **kwargs):
        if "password" in kwargs:
            kwargs["password"] = get_password_hash(kwargs["password"])
        query = (
            update(self._model)
            .where(self._model.id == user_id)
            .values(**kwargs)
            .returning(self._model)
        )
        return session.scalar(query)

    def delete(self, session: Session, user_id: int):
        query = delete(self._model).where(self._model.id == user_id)
        result = session.execute(query)
        return result.rowcount > 0
