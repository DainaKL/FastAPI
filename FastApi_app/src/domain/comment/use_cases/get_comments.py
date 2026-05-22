import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.comment_repository import CommentRepository
from src.schemas.comments import Comment as CommentSchema
from src.core.exceptions.database_exceptions import DatabaseOperationException

logger = logging.getLogger(__name__)


class GetCommentsUseCase:
    def __init__(self) -> None:
        self._repo = CommentRepository()

    async def execute(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        try:
            comments = await self._repo.get_all(db, skip=skip, limit=limit)
            return [CommentSchema.model_validate(c) for c in comments]
        except Exception as e:
            raise DatabaseOperationException("get_all", str(e))
