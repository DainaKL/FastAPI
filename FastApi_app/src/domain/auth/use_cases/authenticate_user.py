from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.core.security import verify_password
from src.core.exceptions.api_exceptions import UserNotFoundException, InvalidPasswordException
import logging

logger = logging.getLogger(__name__)


class AuthenticateUserUseCase:
    def __init__(self):
        self._repo = UserRepository()

    async def execute(self, db: AsyncSession, login: str, password: str):
        user = await self._repo.get_by_login(db, login)
        if not user:
            raise UserNotFoundException(login=login)
        
        logger.info(f"Login attempt for: {login}")
        logger.info(f"Password from request: {password}")
        logger.info(f"Hashed password from DB: {user.password}")
        
        is_valid = verify_password(password, user.password)
        logger.info(f"Verification result: {is_valid}")
        
        if not is_valid:
            raise InvalidPasswordException()
        
        return user