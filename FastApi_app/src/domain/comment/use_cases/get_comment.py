import logging
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.comment_repository import CommentRepository
from src.schemas.comments import Comment as CommentSchema
from src.core.exceptions.api_exceptions import (
    CommentNotFoundException,
    InvalidIDException,
)

logger = logging.getLogger(__name__)


class GetCommentUseCase:
    async def execute(self, db: AsyncSession, comment_id: int) -> CommentSchema:
        if comment_id <= 0:
            raise InvalidIDException(comment_id)

        repo = CommentRepository(db)
        stmt = (
            select(repo.model)
            .where(repo.model.id == comment_id)
            .options(selectinload(repo.model.images))
        )
        result = await db.execute(stmt)
        comment = result.unique().scalar_one_or_none()

        if not comment:
            raise CommentNotFoundException(comment_id=comment_id)
        return CommentSchema.model_validate(comment)
