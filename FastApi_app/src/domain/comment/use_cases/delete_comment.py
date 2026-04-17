import logging

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comment_repository import CommentRepository
from src.core.exceptions.domain_exceptions import CommentNotFoundException as DomainCommentNotFoundException

logger = logging.getLogger(__name__)


class DeleteCommentUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> None:
        try:
            with self._database.session() as session:
                comment = self._repo.get_by_id(session=session, comment_id=comment_id)
                if not comment:
                    error = DomainCommentNotFoundException(comment_id=comment_id)
                    logger.error(error.get_detail())
                    raise error

                self._repo.delete(session=session, comment_id=comment_id)
        except DomainCommentNotFoundException as e:
            raise e
        except DatabaseOperationException as e:
            logger.error(e.get_detail())
            raise
