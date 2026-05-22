import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.post_repository import PostRepository
from src.schemas.posts import Post as PostSchema
from src.core.exceptions.database_exceptions import DatabaseOperationException

logger = logging.getLogger(__name__)


class GetPostsUseCase:
    def __init__(self) -> None:
        self._repo = PostRepository()

    async def execute(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        try:
            posts = await self._repo.get_all(db, skip=skip, limit=limit)
            return [PostSchema.model_validate(p) for p in posts]
        except Exception as e:
            raise DatabaseOperationException("get_all", str(e))
