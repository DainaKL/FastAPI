import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.comment_repository import CommentRepository
from src.infrastructure.sqlite.repositories.post_repository import PostRepository
from src.schemas.comments import Comment as CommentSchema, CommentCreate
from src.core.exceptions.database_exceptions import DatabaseOperationException
from src.core.exceptions.domain_exceptions import PostNotFoundException

logger = logging.getLogger(__name__)


class CreateCommentUseCase:
    def __init__(self) -> None:
        self._repo = CommentRepository()
        self._post_repo = PostRepository()

    async def execute(
        self, db: AsyncSession, comment_data: CommentCreate
    ) -> CommentSchema:
        post = await self._post_repo.get_by_id(db, comment_data.post_id)
        if not post:
            raise PostNotFoundException(post_id=comment_data.post_id)

        try:
            comment = await self._repo.create(db, **comment_data.model_dump())
            await db.flush()
            return CommentSchema.model_validate(comment)
        except Exception as e:
            raise DatabaseOperationException("create", str(e))
