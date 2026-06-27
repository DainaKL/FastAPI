import logging
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.postgres.models.user import User
from src.schemas.users import User as UserSchema
from src.core.exceptions.api_exceptions import UserNotFoundException, InvalidIDException

logger = logging.getLogger(__name__)


class GetUserUseCase:
    async def execute(self, db: AsyncSession, user_id: int) -> UserSchema:
        if user_id <= 0:
            raise InvalidIDException(user_id)

        stmt = select(User).where(User.id == user_id).options(selectinload(User.images))
        result = await db.execute(stmt)
        user = result.unique().scalar_one_or_none()

        if not user:
            raise UserNotFoundException(user_id=user_id)
        return UserSchema.model_validate(user)
