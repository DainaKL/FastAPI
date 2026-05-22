import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.core.exceptions.domain_exceptions import UserNotFoundByIdException

logger = logging.getLogger(__name__)


class DeleteUserUseCase:
    def __init__(self):
        self._repo = UserRepository()

    async def execute(self, db: AsyncSession, user_id: int) -> None:
        user = await self._repo.get_by_id(db, user_id)
        if not user:
            raise UserNotFoundByIdException(user_id)

        await self._repo.delete(db, user_id)
        await db.commit()
