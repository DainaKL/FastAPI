import logging
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.postgres.models.user import User
from src.schemas.users import User as UserSchema
from src.core.exceptions.api_exceptions import (
    InvalidLimitException,
    InvalidSkipException,
    AdminRequiredException,
)

logger = logging.getLogger(__name__)


class GetUsersUseCase:
    async def execute(
        self, db: AsyncSession, skip: int = 0, limit: int = 100, is_admin: bool = False
    ):
        if not is_admin:
            raise AdminRequiredException()

        if skip < 0:
            raise InvalidSkipException(skip)
        if limit < 1 or limit > 100:
            raise InvalidLimitException(limit)

        stmt = select(User).offset(skip).limit(limit).options(selectinload(User.images))
        result = await db.execute(stmt)
        users = result.unique().scalars().all()
        return [UserSchema.model_validate(user) for user in users]
