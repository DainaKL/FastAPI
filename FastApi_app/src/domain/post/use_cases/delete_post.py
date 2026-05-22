import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.post_repository import PostRepository
from src.core.exceptions.database_exceptions import DatabaseOperationException
from src.core.exceptions.domain_exceptions import PostNotFoundException

logger = logging.getLogger(__name__)


class DeletePostUseCase:
    def __init__(self) -> None:
        self._repo = PostRepository()

    async def execute(self, db: AsyncSession, post_id: int) -> None:
        post = await self._repo.get_by_id(db, post_id)
        if not post:
            raise PostNotFoundException(post_id=post_id)

        try:
            await self._repo.delete(db, post_id)
            await db.flush()
        except Exception as e:
            raise DatabaseOperationException("delete", str(e))
