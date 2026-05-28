import logging
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.comment_repository import CommentRepository
from src.schemas.comments import Comment as CommentSchema
from src.core.exceptions.api_exceptions import (
    InvalidLimitException,
    InvalidSkipException,
)

logger = logging.getLogger(__name__)


class GetCommentsUseCase:
    async def execute(
        self, db: AsyncSession, skip: int = 0, limit: int = 100, post_id: int = None
    ):
        if skip < 0:
            raise InvalidSkipException(skip)
        if limit < 1 or limit > 100:
            raise InvalidLimitException(limit)

        repo = CommentRepository(db)
        if post_id:
            stmt = (
                select(repo.model)
                .where(repo.model.post_id == post_id)
                .offset(skip)
                .limit(limit)
                .options(selectinload(repo.model.images))
            )
        else:
            stmt = (
                select(repo.model)
                .offset(skip)
                .limit(limit)
                .options(selectinload(repo.model.images))
            )
        result = await db.execute(stmt)
        comments = result.unique().scalars().all()
        return [CommentSchema.model_validate(c) for c in comments]
