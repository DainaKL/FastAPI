import hashlib
from fastapi import HTTPException, status
from typing import List
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.infrastructure.sqlite.models.users import User as UserModel
from src.schemas.users import UserCreate, UserUpdate, User


class UserUseCases:
    def __init__(self):
        self._database = database

    async def create(self, data: UserCreate) -> User:
        with self._database.session() as session:
            repo = UserRepository(session)
            existing = repo.get_by_login(data.login)
            if existing:
                raise HTTPException(status_code=400, detail="Login already exists")
            hashed_password = hashlib.sha256(data.password.encode()).hexdigest()
            user = UserModel(login=data.login, password=hashed_password)
            created = repo.create(user)
            return User.model_validate(created, from_attributes=True)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        with self._database.session() as session:
            repo = UserRepository(session)
            users = repo.get_all(skip=skip, limit=limit)
            return [User.model_validate(u, from_attributes=True) for u in users]

    async def get_by_id(self, user_id: int) -> User:
        with self._database.session() as session:
            repo = UserRepository(session)
            user = repo.get_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return User.model_validate(user, from_attributes=True)

    async def get_by_login(self, login: str) -> User:
        with self._database.session() as session:
            repo = UserRepository(session)
            user = repo.get_by_login(login)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return User.model_validate(user, from_attributes=True)

    async def update(self, user_id: int, data: UserUpdate) -> User:
        with self._database.session() as session:
            repo = UserRepository(session)
            user = repo.get_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            update_dict = {}
            if data.login:
                update_dict["login"] = data.login
            if data.password:
                update_dict["password"] = hashlib.sha256(
                    data.password.encode()
                ).hexdigest()
            updated = repo.update(user, update_dict)
            return User.model_validate(updated, from_attributes=True)

    async def delete(self, user_id: int) -> None:
        with self._database.session() as session:
            repo = UserRepository(session)
            user = repo.get_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            repo.delete(user)
