import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
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

        repo = UserRepository(db)
        stmt = select(repo.model).offset(skip).limit(limit)
        result = await db.execute(stmt)
        users = result.scalars().all()
        return [UserSchema.model_validate(user) for user in users]
