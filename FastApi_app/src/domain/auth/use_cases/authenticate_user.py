from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.core.security import verify_password
from src.core.exceptions.api_exceptions import (
    UserNotFoundException,
    InvalidPasswordException,
)


class AuthenticateUserUseCase:
    async def execute(self, db: AsyncSession, login: str, password: str):
        user_repo = UserRepository(db)
        user = await user_repo.get_by_login(login)

        if not user:
            raise UserNotFoundException(login=login)

        if not password or not user.password:
            raise InvalidPasswordException()

        if not verify_password(password, user.password):
            raise InvalidPasswordException()

        return user
