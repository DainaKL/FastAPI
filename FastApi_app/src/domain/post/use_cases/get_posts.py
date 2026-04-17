import logging

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post_repository import PostRepository
from src.schemas.posts import Post as PostSchema
from src.core.exceptions.database_exceptions import DatabaseOperationException

logger = logging.getLogger(__name__)


class GetPostsUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = PostRepository()

    async def execute(self, skip: int = 0, limit: int = 100):
        try:
            with self._database.session() as session:
                posts = self._repo.get_all(session=session, skip=skip, limit=limit)
                return [PostSchema.model_validate(p, from_attributes=True) for p in posts]
        except DatabaseOperationException as e:
            logger.error(e.get_detail())
            raise
