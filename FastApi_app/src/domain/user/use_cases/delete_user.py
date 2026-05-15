import logging
from src.core.database import get_async_session
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.core.exceptions.domain_exceptions import UserNotFoundByLoginException

logger = logging.getLogger(__name__)


class DeleteUserUseCase:
    def __init__(self) -> None:
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> None:
        async for session in get_async_session():
            deleted = await self._repo.delete(session=session, user_id=user_id)
            if not deleted:
                raise UserNotFoundByLoginException(login=str(user_id))