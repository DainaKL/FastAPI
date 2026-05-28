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
from src.core.exceptions.api_exceptions import (
    PostNotFoundException,
    CategoryNotFoundException,
    LocationNotFoundException,
    InvalidIDException,
    ForbiddenException,
)

logger = logging.getLogger(__name__)


class UpdatePostUseCase:
    async def execute(
        self,
        db: AsyncSession,
        post_id: int,
        data: PostUpdate,
        current_user_id: int,
        is_admin: bool,
    ):
        if post_id <= 0:
            raise InvalidIDException(post_id)

        repo = PostRepository(db)
        post = await repo.get_by_id(post_id)
        if not post:
            raise PostNotFoundException(post_id=post_id)

        if not is_admin and post.author_id != current_user_id:
            raise ForbiddenException(detail="Вы можете редактировать только свои посты")

        if data.category_id is not None:
            if data.category_id <= 0:
                raise InvalidIDException(data.category_id)
            cat_repo = CategoryRepository(db)
            category = await cat_repo.get_by_id(data.category_id)
            if not category:
                raise CategoryNotFoundException(category_id=data.category_id)
        else:
            data.category_id = None

        if data.location_id is not None:
            if data.location_id <= 0:
                raise InvalidIDException(data.location_id)
            loc_repo = LocationRepository(db)
            location = await loc_repo.get_by_id(data.location_id)
            if not location:
                raise LocationNotFoundException(location_id=data.location_id)
        else:
            data.location_id = None

        update_dict = {k: v for k, v in data.model_dump().items() if v is not None}
        if not update_dict:
            return PostSchema.model_validate(post)

        updated = await repo.update(post_id, **update_dict)
        await db.commit()
        return PostSchema.model_validate(updated)
