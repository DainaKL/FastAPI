import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.postgres.repositories.comment_repository import (
    CommentRepository,
)
from src.schemas.comments import Comment as CommentSchema

logger = logging.getLogger(__name__)


class GetCommentsByPostUseCase:
    def __init__(self) -> None:
        self._repo = CommentRepository()

    async def execute(
        self, db: AsyncSession, post_id: int, skip: int = 0, limit: int = 100
    ):
        comments = await self._repo.get_by_post(db, post_id, skip=skip, limit=limit)
        return [CommentSchema.model_validate(c) for c in comments]
