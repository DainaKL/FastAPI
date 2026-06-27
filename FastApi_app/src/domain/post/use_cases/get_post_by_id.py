import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.postgres.repositories.post_repository import PostRepository
from src.schemas.posts import Post as PostSchema
from src.core.exceptions.database_exceptions import DatabaseOperationException
from src.core.exceptions.domain_exceptions import PostNotFoundException

logger = logging.getLogger(__name__)


class GetPostByIdUseCase:
    def __init__(self) -> None:
        self._repo = PostRepository()

    async def execute(self, db: AsyncSession, post_id: int) -> PostSchema:
        try:
            post = await self._repo.get_by_id(db, post_id)
            if not post:
                raise PostNotFoundException(post_id=post_id)
            return PostSchema.model_validate(post)
        except PostNotFoundException as e:
            raise e
        except Exception as e:
            raise DatabaseOperationException("get_by_id", str(e))
