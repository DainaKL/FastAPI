from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.user.use_cases.get_users import GetUsersUseCase
from src.domain.user.use_cases.get_user import GetUserUseCase
from src.domain.user.use_cases.create_user import CreateUserUseCase
from src.domain.user.use_cases.update_user import UpdateUserUseCase
from src.domain.user.use_cases.delete_user import DeleteUserUseCase


class UserUseCases:
    def __init__(self):
        self._get_all = GetUsersUseCase()
        self._get_by_id = GetUserUseCase()
        self._create = CreateUserUseCase()
        self._update = UpdateUserUseCase()
        self._delete = DeleteUserUseCase()

    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        return await self._get_all.execute(db, skip=skip, limit=limit)

    async def get_by_id(self, db: AsyncSession, user_id: int):
        return await self._get_by_id.execute(db, user_id)

    async def create(self, db: AsyncSession, login: str, password: str):
        return await self._create.execute(db, login, password)

    async def update(self, db: AsyncSession, user_id: int, user_data):
        return await self._update.execute(db, user_id, user_data)

    async def delete(self, db: AsyncSession, user_id: int):
        return await self._delete.execute(db, user_id)
