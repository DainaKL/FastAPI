import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.comment_repository import CommentRepository
from src.schemas.comments import Comment as CommentSchema, CommentUpdate
from src.core.exceptions.api_exceptions import CommentNotFoundException

logger = logging.getLogger(__name__)


class UpdateCommentUseCase:
    def __init__(self, repo: CommentRepository):
        self._repo = repo

    async def execute(self, db: AsyncSession, comment_id: int, data: dict) -> CommentSchema:
        comment = await self._repo.get_by_id(db, comment_id)
        if not comment:
            raise CommentNotFoundException(comment_id=comment_id)

        if data:
            updated = await self._repo.update(db, comment_id, **data)
            await db.flush()
            return CommentSchema.model_validate(updated)
        return CommentSchema.model_validate(comment)
