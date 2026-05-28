import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.comment_repository import CommentRepository
from src.core.exceptions.api_exceptions import (
    CommentNotFoundException,
    CommentForbiddenException,
    InvalidIDException,
)

logger = logging.getLogger(__name__)


class DeleteCommentUseCase:
    async def execute(
        self, db: AsyncSession, comment_id: int, current_user_id: int, is_admin: bool
    ):
        if comment_id <= 0:
            raise InvalidIDException(comment_id)

        repo = CommentRepository(db)
        comment = await repo.get_by_id(comment_id)
        if not comment:
            raise CommentNotFoundException(comment_id=comment_id)

        if not is_admin and comment.author_id != current_user_id:
            raise CommentForbiddenException(action="удалять")

        await repo.delete(comment_id)
        await db.commit()
