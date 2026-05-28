import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.schemas.users import User as UserSchema
from src.core.exceptions.api_exceptions import UserAlreadyExistsException
from src.core.security import get_password_hash

logger = logging.getLogger(__name__)


class CreateUserUseCase:
    async def execute(self, db: AsyncSession, login: str, password: str) -> UserSchema:
        repo = UserRepository(db)

        if await repo.exists_by_login(login):
            raise UserAlreadyExistsException(login=login)

        hashed_password = get_password_hash(password)
        user = await repo.create_user(login=login, password=hashed_password)
        await db.commit()
        return UserSchema.model_validate(user)
