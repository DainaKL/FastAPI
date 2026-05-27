import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.comment_repository import CommentRepository
from src.schemas.comments import Comment as CommentSchema
from src.core.exceptions.api_exceptions import CommentNotFoundException

logger = logging.getLogger(__name__)


class GetCommentUseCase:
    def __init__(self) -> None:
        self._repo = CommentRepository()

    async def execute(self, db: AsyncSession, comment_id: int) -> CommentSchema:
        comment = await self._repo.get_by_id(db, comment_id)
        if not comment:
            raise CommentNotFoundException(comment_id=comment_id)
        return CommentSchema.model_validate(comment)
