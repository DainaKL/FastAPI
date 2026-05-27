import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.comment_repository import CommentRepository
from src.core.exceptions.api_exceptions import CommentNotFoundException

logger = logging.getLogger(__name__)


class DeleteCommentUseCase:
    def __init__(self, repo: CommentRepository):
        self._repo = repo

    async def execute(self, db: AsyncSession, comment_id: int) -> None:
        comment = await self._repo.get_by_id(db, comment_id)
        if not comment:
            raise CommentNotFoundException(comment_id=comment_id)

        await self._repo.delete(db, comment_id)
        await db.flush()
