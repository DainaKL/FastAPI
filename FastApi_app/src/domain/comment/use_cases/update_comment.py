import logging

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comment_repository import CommentRepository
from src.schemas.comments import Comment as CommentSchema, CommentUpdate
from src.core.exceptions.database_exceptions import DatabaseOperationException
from src.core.exceptions.domain_exceptions import (
    CommentNotFoundException as DomainCommentNotFoundException,
)

logger = logging.getLogger(__name__)


class UpdateCommentUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int, data: CommentUpdate) -> CommentSchema:
        try:
            with self._database.session() as session:
                comment = self._repo.get_by_id(session=session, comment_id=comment_id)
                if not comment:
                    error = DomainCommentNotFoundException(comment_id=comment_id)
                    logger.error(error.get_detail())
                    raise error

                update_dict = {
                    k: v for k, v in data.model_dump().items() if v is not None
                }
                updated = self._repo.update(
                    session=session, comment_id=comment_id, **update_dict
                )
                return CommentSchema.model_validate(updated, from_attributes=True)
        except DomainCommentNotFoundException as e:
            raise e
        except DatabaseOperationException as e:
            logger.error(e.get_detail())
            raise
