import logging

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post_repository import PostRepository
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.infrastructure.sqlite.repositories.category_repository import CategoryRepository
from src.infrastructure.sqlite.repositories.location_repository import LocationRepository
from src.schemas.posts import Post as PostSchema, PostCreate
from src.core.exceptions.database_exceptions import (
    DatabaseOperationException,
)
from src.core.exceptions.domain_exceptions import (
    UserNotFoundByLoginException,
    CategoryNotFoundException as DomainCategoryNotFoundException,
    LocationNotFoundException as DomainLocationNotFoundException,
)

logger = logging.getLogger(__name__)


class CreatePostUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = PostRepository()
        self._user_repo = UserRepository()
        self._category_repo = CategoryRepository()
        self._location_repo = LocationRepository()

    async def execute(self, data: PostCreate) -> PostSchema:
        try:
            with self._database.session() as session:
                user = self._user_repo.get_by_id(session=session, user_id=data.author_id)
                if not user:
                    error = UserNotFoundByLoginException(login=str(data.author_id))
                    logger.error(error.get_detail())
                    raise error

                if data.category_id:
                    category = self._category_repo.get_by_id(session=session, category_id=data.category_id)
                    if not category:
                        error = DomainCategoryNotFoundException(category_id=data.category_id)
                        logger.error(error.get_detail())
                        raise error

                if data.location_id:
                    location = self._location_repo.get_by_id(session=session, location_id=data.location_id)
                    if not location:
                        error = DomainLocationNotFoundException(location_id=data.location_id)
                        logger.error(error.get_detail())
                        raise error

                post_dict = data.model_dump()
                post = self._repo.create(session=session, **post_dict)
                return PostSchema.model_validate(post, from_attributes=True)
        except (UserNotFoundByLoginException, DomainCategoryNotFoundException, DomainLocationNotFoundException) as e:
            raise e
        except DatabaseOperationException as e:
            logger.error(e.get_detail())
            raise
