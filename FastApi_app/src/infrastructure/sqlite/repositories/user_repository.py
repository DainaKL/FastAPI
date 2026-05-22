from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlite.models.users import User as UserModel
from src.infrastructure.sqlite.repositories.base import BaseRepository
from src.core.security import get_password_hash


class UserRepository(BaseRepository[UserModel]):
    def __init__(self):
        super().__init__(UserModel)

    async def get_by_login(
        self, session: AsyncSession, login: str
    ) -> Optional[UserModel]:
        if not login:
            return None
        stmt = select(self.model).where(self.model.login == login)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def exists_by_login(self, session: AsyncSession, login: str) -> bool:
        if not login:
            return False
        stmt = select(self.model).where(self.model.login == login)
        result = await session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def create_user(
        self, session: AsyncSession, login: str, password: str, is_admin: bool = False
    ) -> UserModel:
        hashed_password = get_password_hash(password)
        return await self.create(
            session, login=login, password=hashed_password, is_admin=is_admin
        )
