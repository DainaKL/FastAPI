from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlite.models.user import User
from src.infrastructure.sqlite.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_by_id(self, user_id: int) -> Optional[User]:
        return await super().get_by_id(user_id)

    async def get_by_login(self, login: str) -> Optional[User]:
        result = await self.session.execute(
            select(self.model).where(self.model.login == login)
        )
        return result.scalar_one_or_none()

    async def exists_by_login(self, login: str) -> bool:
        result = await self.session.execute(
            select(self.model).where(self.model.login == login)
        )
        return result.scalar_one_or_none() is not None

    async def create_user(
        self, login: str, password: str, is_admin: bool = False
    ) -> User:
        # Здесь НЕ хешируем! Пароль уже хеширован в use case
        return await self.create(login=login, password=password, is_admin=is_admin)
