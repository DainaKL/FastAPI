import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.comment_repository import CommentRepository
from src.core.exceptions.database_exceptions import DatabaseOperationException
from src.core.exceptions.domain_exceptions import CommentNotFoundException

logger = logging.getLogger(__name__)


class DeleteCommentUseCase:
    def __init__(self) -> None:
        self._repo = CommentRepository()

    async def execute(self, db: AsyncSession, comment_id: int) -> None:
        comment = await self._repo.get_by_id(db, comment_id)
        if not comment:
            raise CommentNotFoundException(comment_id=comment_id)

        try:
            await self._repo.delete(db, comment_id)
            await db.flush()
        except Exception as e:
            raise DatabaseOperationException("delete", str(e))
