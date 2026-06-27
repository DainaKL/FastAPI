import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.postgres.repositories.comment_repository import (
    CommentRepository,
)
from src.schemas.comments import Comment as CommentSchema, CommentUpdate
from src.core.exceptions.api_exceptions import (
    CommentNotFoundException,
    CommentForbiddenException,
    InvalidIDException,
)

logger = logging.getLogger(__name__)


class UpdateCommentUseCase:
    async def execute(
        self,
        db: AsyncSession,
        comment_id: int,
        data: CommentUpdate,
        current_user_id: int,
        is_admin: bool,
    ):
        if comment_id <= 0:
            raise InvalidIDException(comment_id)

        repo = CommentRepository(db)
        comment = await repo.get_by_id(comment_id)
        if not comment:
            raise CommentNotFoundException(comment_id=comment_id)

        if not is_admin and comment.author_id != current_user_id:
            raise CommentForbiddenException(action="редактировать")

        update_dict = {k: v for k, v in data.model_dump().items() if v is not None}
        if update_dict:
            await repo.update(comment_id, **update_dict)
            await db.commit()

        return CommentSchema.model_validate(comment)
