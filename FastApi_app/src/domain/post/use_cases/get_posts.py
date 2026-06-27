import logging
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.postgres.repositories.post_repository import PostRepository
from src.schemas.posts import Post as PostSchema
from src.core.exceptions.api_exceptions import (
    InvalidLimitException,
    InvalidSkipException,
)

logger = logging.getLogger(__name__)


class GetPostsUseCase:
    async def execute(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        if skip < 0:
            raise InvalidSkipException(skip)
        if limit < 1 or limit > 100:
            raise InvalidLimitException(limit)

        repo = PostRepository(db)
        stmt = (
            select(repo.model)
            .offset(skip)
            .limit(limit)
            .options(
                selectinload(repo.model.images),
                selectinload(repo.model.author),
                selectinload(repo.model.location),
                selectinload(repo.model.category),
            )
        )
        result = await db.execute(stmt)
        posts = result.unique().scalars().all()
        return [PostSchema.model_validate(p) for p in posts]
