import logging

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comment_repository import CommentRepository
from src.schemas.comments import Comment as CommentSchema
from src.core.exceptions.database_exceptions import CommentNotFoundException
from src.core.exceptions.domain_exceptions import (
    CommentNotFoundException as DomainCommentNotFoundException,
)

logger = logging.getLogger(__name__)


class GetCommentUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> CommentSchema:
        try:
            with self._database.session() as session:
                comment = self._repo.get_by_id(session=session, comment_id=comment_id)
                return CommentSchema.model_validate(comment, from_attributes=True)
        except CommentNotFoundException:
            error = DomainCommentNotFoundException(comment_id=comment_id)
            logger.error(error.get_detail())
            raise error
