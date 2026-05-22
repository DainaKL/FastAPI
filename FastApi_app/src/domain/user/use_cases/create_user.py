from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.schemas.users import User as UserSchema
from src.core.exceptions.domain_exceptions import UserLoginIsNotUniqueException


class CreateUserUseCase:
    def __init__(self):
        self._repo = UserRepository()

    async def execute(self, db: AsyncSession, login: str, password: str) -> UserSchema:
        if await self._repo.exists_by_login(db, login):
            raise UserLoginIsNotUniqueException(login=login)

        user = await self._repo.create_user(db, login=login, password=password)
        await db.commit()
        return UserSchema.model_validate(user)
