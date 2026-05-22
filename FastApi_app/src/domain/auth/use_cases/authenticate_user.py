from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.core.security import verify_password
from src.core.exceptions.domain_exceptions import UserNotFoundByLoginException
from src.core.exceptions.auth_exceptions import InvalidPasswordException


class AuthenticateUserUseCase:
    async def execute(self, db: AsyncSession, login: str, password: str):
        repo = UserRepository()
        user = await repo.get_by_login(db, login)
        if not user:
            raise UserNotFoundByLoginException(login=login)

        if not verify_password(password, user.password):
            raise InvalidPasswordException()

        return user
