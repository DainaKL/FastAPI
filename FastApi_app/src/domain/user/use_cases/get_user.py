import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.schemas.users import User as UserSchema
from src.core.exceptions.api_exceptions import UserNotFoundException, InvalidIDException

logger = logging.getLogger(__name__)


class GetUserUseCase:
    async def execute(self, db: AsyncSession, user_id: int) -> UserSchema:
        if user_id <= 0:
            raise InvalidIDException(user_id)

        repo = UserRepository(db)
        stmt = select(repo.model).where(repo.model.id == user_id)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise UserNotFoundException(user_id=user_id)
        return UserSchema.model_validate(user)
