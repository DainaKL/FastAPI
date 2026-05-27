from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.schemas.users import User as UserSchema
from typing import List


class GetUsersUseCase:
    def __init__(self):
        self._repo = UserRepository()

    async def execute(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[UserSchema]:
        users = await self._repo.get_all(db, skip=skip, limit=limit)
        return [UserSchema.model_validate(user) for user in users]
