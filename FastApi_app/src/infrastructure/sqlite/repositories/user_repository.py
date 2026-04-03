from typing import List, Optional
from sqlalchemy.orm import Session
from src.infrastructure.sqlite.models.users import User as UserModel


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: UserModel) -> UserModel:
        self.session.add(user)
        self.session.flush()
        return user

    def get_all(self, skip: int = 0, limit: int = 100) -> List[UserModel]:
        return self.session.query(UserModel).offset(skip).limit(limit).all()

    def get_by_id(self, user_id: int) -> Optional[UserModel]:
        return self.session.query(UserModel).filter(UserModel.id == user_id).first()

    def get_by_login(self, login: str) -> Optional[UserModel]:
        return self.session.query(UserModel).filter(UserModel.login == login).first()

    def update(self, user: UserModel, data: dict) -> UserModel:
        for key, value in data.items():
            setattr(user, key, value)
        self.session.flush()
        return user

    def delete(self, user: UserModel) -> None:
        self.session.delete(user)
        self.session.flush()
