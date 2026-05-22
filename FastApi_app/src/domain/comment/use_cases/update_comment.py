import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.comment_repository import CommentRepository
from src.schemas.comments import Comment as CommentSchema, CommentUpdate
from src.core.exceptions.database_exceptions import DatabaseOperationException
from src.core.exceptions.domain_exceptions import CommentNotFoundException

logger = logging.getLogger(__name__)


class UpdateCommentUseCase:
    def __init__(self) -> None:
        self._repo = CommentRepository()

    async def execute(
        self, db: AsyncSession, comment_id: int, data: CommentUpdate
    ) -> CommentSchema:
        comment = await self._repo.get_by_id(db, comment_id)
        if not comment:
            raise CommentNotFoundException(comment_id=comment_id)

        update_dict = {k: v for k, v in data.model_dump().items() if v is not None}
        if not update_dict:
            return CommentSchema.model_validate(comment)

        try:
            updated = await self._repo.update(db, comment_id, **update_dict)
            await db.flush()
            return CommentSchema.model_validate(updated)
        except Exception as e:
            raise DatabaseOperationException("update", str(e))
