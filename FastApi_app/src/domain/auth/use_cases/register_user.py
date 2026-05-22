from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.core.exceptions.domain_exceptions import UserLoginIsNotUniqueException


class RegisterUserUseCase:
    async def execute(self, db: AsyncSession, login: str, password: str):
        repo = UserRepository()

        if await repo.exists_by_login(db, login):
            raise UserLoginIsNotUniqueException(login=login)

        user = await repo.create_user(db, login=login, password=password)
        await db.commit()

        return user
