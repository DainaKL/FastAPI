import logging
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.postgres.repositories.post_repository import PostRepository
from src.schemas.posts import Post as PostSchema
from src.core.exceptions.api_exceptions import PostNotFoundException, InvalidIDException

logger = logging.getLogger(__name__)


class GetPostUseCase:
    async def execute(self, db: AsyncSession, post_id: int) -> PostSchema:
        if post_id <= 0:
            raise InvalidIDException(post_id)

        repo = PostRepository(db)
        stmt = (
            select(repo.model)
            .where(repo.model.id == post_id)
            .options(
                selectinload(repo.model.images),
                selectinload(repo.model.author),
                selectinload(repo.model.location),
                selectinload(repo.model.category),
            )
        )
        result = await db.execute(stmt)
        post = result.unique().scalar_one_or_none()

        if not post:
            raise PostNotFoundException(post_id=post_id)
        return PostSchema.model_validate(post)
