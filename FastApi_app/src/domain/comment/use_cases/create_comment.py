import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.comment_repository import CommentRepository
from src.infrastructure.sqlite.repositories.post_repository import PostRepository
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.schemas.comments import Comment as CommentSchema
from src.core.exceptions.api_exceptions import PostNotFoundException, UserNotFoundException

logger = logging.getLogger(__name__)


class CreateCommentUseCase:
    def __init__(self, repo: CommentRepository, post_repo: PostRepository, user_repo: UserRepository):
        self._repo = repo
        self._post_repo = post_repo
        self._user_repo = user_repo

    async def execute(self, db: AsyncSession, comment_data: dict) -> CommentSchema:
        user = await self._user_repo.get_by_id(db, comment_data["author_id"])
        if not user:
            raise UserNotFoundException(user_id=comment_data["author_id"])

        post = await self._post_repo.get_by_id(db, comment_data["post_id"])
        if not post:
            raise PostNotFoundException(post_id=comment_data["post_id"])

        comment = await self._repo.create(db, **comment_data)
        await db.flush()
        return CommentSchema.model_validate(comment)
