import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.core.exceptions.api_exceptions import UserNotFoundException

logger = logging.getLogger(__name__)


class DeleteUserUseCase:
    def __init__(self):
        self._repo = UserRepository()

    async def execute(self, db: AsyncSession, user_id: int) -> None:
        user = await self._repo.get_by_id(db, user_id)
        if not user:
            raise UserNotFoundException(user_id=user_id)

        await self._repo.delete(db, user_id)
        await db.commit()
