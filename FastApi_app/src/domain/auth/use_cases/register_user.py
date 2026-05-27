from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.core.security import get_password_hash
from src.core.exceptions.api_exceptions import UserAlreadyExistsException


class RegisterUserUseCase:
    def __init__(self):
        self._repo = UserRepository()

    async def execute(self, db: AsyncSession, login: str, password: str):
        if await self._repo.exists_by_login(db, login):
            raise UserAlreadyExistsException(login=login)
        
        hashed_password = get_password_hash(password)
        user = await self._repo.create_user(db, login=login, password=hashed_password)
        await db.commit()
        return user
