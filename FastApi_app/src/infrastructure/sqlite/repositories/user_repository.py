from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import Session
from src.infrastructure.sqlite.models.users import User as UserModel
from src.schemas.users import UserCreate as UserSchema
from src.core.exceptions.database_exceptions import UserAlreadyExistsException
from src.core.security import get_password_hash


class UserRepository:
    def get_by_id(self, session: Session, user_id: int):
        if user_id <= 0:
            return None
        query = select(UserModel).where(UserModel.id == user_id)
        return session.execute(query).scalar_one_or_none()

    def get_by_login(self, session: Session, login: str):
        if not login:
            return None
        query = select(UserModel).where(UserModel.login == login)
        return session.execute(query).scalar_one_or_none()

    def exists_by_login(self, session: Session, login: str) -> bool:
        if not login:
            return False
        query = select(UserModel).where(UserModel.login == login)
        return session.execute(query).scalar_one_or_none() is not None

    def get_all(self, session: Session, skip: int = 0, limit: int = 100):
        query = select(UserModel).offset(skip).limit(limit)
        return list(session.execute(query).scalars().all())

    def create(self, session: Session, user: UserSchema) -> UserModel:
        user_dict = user.model_dump()
        user_dict["password"] = get_password_hash(user_dict["password"])
        query = insert(UserModel).values(**user_dict).returning(UserModel)
        result = session.execute(query)
        session.commit()
        return result.scalar_one()

    def update(self, session: Session, user_id: int, **kwargs):
        if "password" in kwargs:
            kwargs["password"] = get_password_hash(kwargs["password"])
        query = update(UserModel).where(UserModel.id == user_id).values(**kwargs).returning(UserModel)
        result = session.execute(query)
        session.commit()
        return result.scalar_one_or_none()

    def delete(self, session: Session, user_id: int):
        query = delete(UserModel).where(UserModel.id == user_id)
        result = session.execute(query)
        session.commit()
        return result.rowcount > 0