import logging

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comment_repository import CommentRepository
from src.schemas.comments import Comment as CommentSchema
from src.core.exceptions.database_exceptions import DatabaseOperationException

logger = logging.getLogger(__name__)


class GetCommentsUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, skip: int = 0, limit: int = 100):
        try:
            with self._database.session() as session:
                comments = self._repo.get_all(session=session, skip=skip, limit=limit)
                return [CommentSchema.model_validate(c, from_attributes=True) for c in comments]
        except DatabaseOperationException as e:
            logger.error(e.get_detail())
            raise
