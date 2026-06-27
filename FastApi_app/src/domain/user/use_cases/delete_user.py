import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.postgres.repositories.user_repository import UserRepository
from src.core.exceptions.api_exceptions import (
    UserNotFoundException,
    ForbiddenException,
    InvalidIDException,
)

logger = logging.getLogger(__name__)


class DeleteUserUseCase:
    async def execute(
        self, db: AsyncSession, user_id: int, current_user_id: int, is_admin: bool
    ):
        if user_id <= 0:
            raise InvalidIDException(user_id)

        repo = UserRepository(db)
        user = await repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id=user_id)

        if not is_admin and current_user_id != user_id:
            raise ForbiddenException(detail="Вы можете удалить только свой профиль")

        await repo.delete(user_id)
        await db.commit()
