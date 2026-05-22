import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.post_repository import PostRepository
from src.infrastructure.sqlite.repositories.category_repository import (
    CategoryRepository,
)
from src.infrastructure.sqlite.repositories.location_repository import (
    LocationRepository,
)
from src.schemas.posts import Post as PostSchema, PostUpdate
from src.core.exceptions.database_exceptions import DatabaseOperationException
from src.core.exceptions.domain_exceptions import (
    PostNotFoundException,
    CategoryNotFoundException,
    LocationNotFoundException,
)

logger = logging.getLogger(__name__)


class UpdatePostUseCase:
    def __init__(self) -> None:
        self._repo = PostRepository()
        self._category_repo = CategoryRepository()
        self._location_repo = LocationRepository()

    async def execute(
        self, db: AsyncSession, post_id: int, data: PostUpdate
    ) -> PostSchema:
        post = await self._repo.get_by_id(db, post_id)
        if not post:
            raise PostNotFoundException(post_id=post_id)

        if data.category_id is not None:
            category = await self._category_repo.get_by_id(db, data.category_id)
            if not category:
                raise CategoryNotFoundException(category_id=data.category_id)

        if data.location_id is not None:
            location = await self._location_repo.get_by_id(db, data.location_id)
            if not location:
                raise LocationNotFoundException(location_id=data.location_id)

        update_dict = {k: v for k, v in data.model_dump().items() if v is not None}
        if not update_dict:
            return PostSchema.model_validate(post)

        try:
            updated = await self._repo.update(db, post_id, **update_dict)
            await db.flush()
            return PostSchema.model_validate(updated)
        except Exception as e:
            raise DatabaseOperationException("update", str(e))
