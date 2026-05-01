import logging

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post_repository import PostRepository
from src.schemas.posts import Post as PostSchema
from src.core.exceptions.database_exceptions import PostNotFoundException
from src.core.exceptions.domain_exceptions import (
    PostNotFoundException as DomainPostNotFoundException,
)

logger = logging.getLogger(__name__)


class GetPostUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> PostSchema:
        try:
            with self._database.session() as session:
                post = self._repo.get_by_id(session=session, post_id=post_id)
                return PostSchema.model_validate(post, from_attributes=True)
        except PostNotFoundException:
            error = DomainPostNotFoundException(post_id=post_id)
            logger.error(error.get_detail())
            raise error
