import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.post_repository import PostRepository
from src.core.exceptions.api_exceptions import (
    PostNotFoundException,
    InvalidIDException,
    ForbiddenException,
)

logger = logging.getLogger(__name__)


class DeletePostUseCase:
    async def execute(
        self, db: AsyncSession, post_id: int, current_user_id: int, is_admin: bool
    ):
        if post_id <= 0:
            raise InvalidIDException(post_id)

        repo = PostRepository(db)
        post = await repo.get_by_id(post_id)
        if not post:
            raise PostNotFoundException(post_id=post_id)

        if not is_admin and post.author_id != current_user_id:
            raise ForbiddenException(detail="Вы можете удалять только свои посты")

        await repo.delete(post_id)
        await db.commit()
