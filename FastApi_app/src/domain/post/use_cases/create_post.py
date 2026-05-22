import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.post_repository import PostRepository
from src.infrastructure.sqlite.repositories.category_repository import (
    CategoryRepository,
)
from src.infrastructure.sqlite.repositories.location_repository import (
    LocationRepository,
)
from src.schemas.posts import Post as PostSchema, PostCreate
from src.core.exceptions.database_exceptions import DatabaseOperationException
from src.core.exceptions.domain_exceptions import (
    CategoryNotFoundException,
    LocationNotFoundException,
)

logger = logging.getLogger(__name__)


class CreatePostUseCase:
    def __init__(self) -> None:
        self._repo = PostRepository()
        self._category_repo = CategoryRepository()
        self._location_repo = LocationRepository()

    async def execute(self, db: AsyncSession, post_data: PostCreate) -> PostSchema:
        if post_data.category_id is not None:
            category = await self._category_repo.get_by_id(db, post_data.category_id)
            if not category:
                raise CategoryNotFoundException(category_id=post_data.category_id)

        if post_data.location_id is not None:
            location = await self._location_repo.get_by_id(db, post_data.location_id)
            if not location:
                raise LocationNotFoundException(location_id=post_data.location_id)

        try:
            post = await self._repo.create(db, **post_data.model_dump())
            await db.flush()
            return PostSchema.model_validate(post)
        except Exception as e:
            raise DatabaseOperationException("create", str(e))
