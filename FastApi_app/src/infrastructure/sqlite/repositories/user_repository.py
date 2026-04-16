from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from src.core.exceptions.database_exceptions import (
    DatabaseOperationException, UserAlreadyExistsException,
    UserNotFoundException)
from src.infrastructure.sqlite.models.users import User as UserModel


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_login(self, login: str) -> UserModel:
        try:
            stmt = select(UserModel).where(UserModel.login == login)
            user = self.session.execute(stmt).scalar_one_or_none()
            if not user:
                raise UserNotFoundException(login=login)
            return user
        except UserNotFoundException:
            raise
        except SQLAlchemyError as e:
            raise DatabaseOperationException("get_by_login", str(e))

    def get_by_id(self, user_id: int) -> UserModel:
        try:
            user = self.session.get(UserModel, user_id)
            if not user:
                raise UserNotFoundException(user_id=user_id)
            return user
        except UserNotFoundException:
            raise
        except SQLAlchemyError as e:
            raise DatabaseOperationException("get_by_id", str(e))

    def create(self, login: str, password: str) -> UserModel:
        try:
            user = UserModel(login=login, password=password)
            self.session.add(user)
            self.session.flush()
            self.session.refresh(user)
            return user
        except IntegrityError:
            self.session.rollback()
            raise UserAlreadyExistsException(login=login)
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseOperationException("create", str(e))

    def update(self, user_id: int, **kwargs) -> UserModel:
        try:
            user = self.get_by_id(user_id)
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            self.session.flush()
            self.session.refresh(user)
            return user
        except UserNotFoundException:
            raise
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseOperationException("update", str(e))

    def delete(self, user_id: int) -> None:
        try:
            user = self.get_by_id(user_id)
            self.session.delete(user)
            self.session.flush()
        except UserNotFoundException:
            raise
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseOperationException("delete", str(e))
