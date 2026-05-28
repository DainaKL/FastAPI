from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.core.security import get_password_hash
from src.core.exceptions.api_exceptions import UserAlreadyExistsException


class RegisterUserUseCase:
    async def execute(self, db: AsyncSession, login: str, password: str):
        user_repo = UserRepository(db)

        if await user_repo.exists_by_login(login):
            raise UserAlreadyExistsException(login=login)

        hashed_password = get_password_hash(password)
        user = await user_repo.create_user(login=login, password=hashed_password)
        await db.commit()
        return user
