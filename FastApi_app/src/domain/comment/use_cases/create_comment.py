import logging
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.comment_repository import CommentRepository
from src.infrastructure.sqlite.repositories.post_repository import PostRepository
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.schemas.comments import Comment as CommentSchema
from src.core.exceptions.api_exceptions import (
    PostNotFoundException,
    UserNotFoundException,
    InvalidIDException,
)

logger = logging.getLogger(__name__)


class CreateCommentUseCase:
    async def execute(
        self,
        db: AsyncSession,
        text: str,
        post_id: int,
        is_published: bool,
        author_id: int,
    ):
        if author_id <= 0:
            raise InvalidIDException(author_id)
        if post_id <= 0:
            raise InvalidIDException(post_id)

        user_repo = UserRepository(db)
        user = await user_repo.get_by_id(author_id)
        if not user:
            raise UserNotFoundException(user_id=author_id)

        post_repo = PostRepository(db)
        post = await post_repo.get_by_id(post_id)
        if not post:
            raise PostNotFoundException(post_id=post_id)

        comment_repo = CommentRepository(db)
        comment = await comment_repo.create(
            text=text, post_id=post_id, author_id=author_id, is_published=is_published
        )

        await db.commit()

        stmt = (
            select(comment_repo.model)
            .where(comment_repo.model.id == comment.id)
            .options(selectinload(comment_repo.model.images))
        )
        result = await db.execute(stmt)
        comment_with_images = result.unique().scalar_one()

        return CommentSchema.model_validate(comment_with_images)
