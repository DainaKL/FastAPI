import logging

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post_repository import PostRepository
from src.core.exceptions.domain_exceptions import PostNotFoundException as DomainPostNotFoundException

logger = logging.getLogger(__name__)


class DeletePostUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> None:
        try:
            with self._database.session() as session:
                post = self._repo.get_by_id(session=session, post_id=post_id)
                if not post:
                    error = DomainPostNotFoundException(post_id=post_id)
                    logger.error(error.get_detail())
                    raise error

                self._repo.delete(session=session, post_id=post_id)
        except DomainPostNotFoundException as e:
            raise e
        except DatabaseOperationException as e:
            logger.error(e.get_detail())
            raise
