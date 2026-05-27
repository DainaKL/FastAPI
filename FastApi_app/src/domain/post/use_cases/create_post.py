import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlite.repositories.post_repository import PostRepository
from src.infrastructure.sqlite.repositories.category_repository import CategoryRepository
from src.infrastructure.sqlite.repositories.location_repository import LocationRepository
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.schemas.posts import Post as PostSchema, PostCreate
from src.core.exceptions.api_exceptions import CategoryNotFoundException, LocationNotFoundException, UserNotFoundException

logger = logging.getLogger(__name__)


class CreatePostUseCase:
    def __init__(self) -> None:
        self._repo = PostRepository()
        self._category_repo = CategoryRepository()
        self._location_repo = LocationRepository()
        self._user_repo = UserRepository()

    async def execute(self, db: AsyncSession, post_data: PostCreate) -> PostSchema:
        user = await self._user_repo.get_by_id(db, post_data.author_id)
        if not user:
            raise UserNotFoundException(user_id=post_data.author_id)

        if post_data.category_id is not None and post_data.category_id > 0:
            category = await self._category_repo.get_by_id(db, post_data.category_id)
            if not category:
                raise CategoryNotFoundException(category_id=post_data.category_id)
        else:
            post_data.category_id = None

        if post_data.location_id is not None and post_data.location_id > 0:
            location = await self._location_repo.get_by_id(db, post_data.location_id)
            if not location:
                raise LocationNotFoundException(location_id=post_data.location_id)
        else:
            post_data.location_id = None

        post = await self._repo.create(db, **post_data.model_dump())
        await db.flush()
        return PostSchema.model_validate(post)
