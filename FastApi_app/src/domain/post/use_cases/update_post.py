import logging

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post_repository import PostRepository
from src.infrastructure.sqlite.repositories.category_repository import CategoryRepository
from src.infrastructure.sqlite.repositories.location_repository import LocationRepository
from src.schemas.posts import Post as PostSchema, PostUpdate
from src.core.exceptions.database_exceptions import (
    DatabaseOperationException,
)
from src.core.exceptions.domain_exceptions import (
    PostNotFoundException as DomainPostNotFoundException,
    CategoryNotFoundException as DomainCategoryNotFoundException,
    LocationNotFoundException as DomainLocationNotFoundException,
)

logger = logging.getLogger(__name__)


class UpdatePostUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = PostRepository()
        self._category_repo = CategoryRepository()
        self._location_repo = LocationRepository()

    async def execute(self, post_id: int, data: PostUpdate) -> PostSchema:
        try:
            with self._database.session() as session:
                post = self._repo.get_by_id(session=session, post_id=post_id)
                if not post:
                    error = DomainPostNotFoundException(post_id=post_id)
                    logger.error(error.get_detail())
                    raise error

                if data.category_id is not None:
                    category = self._category_repo.get_by_id(session=session, category_id=data.category_id)
                    if not category:
                        error = DomainCategoryNotFoundException(category_id=data.category_id)
                        logger.error(error.get_detail())
                        raise error

                if data.location_id is not None:
                    location = self._location_repo.get_by_id(session=session, location_id=data.location_id)
                    if not location:
                        error = DomainLocationNotFoundException(location_id=data.location_id)
                        logger.error(error.get_detail())
                        raise error

                update_dict = {k: v for k, v in data.model_dump().items() if v is not None}
                updated = self._repo.update(session=session, post_id=post_id, **update_dict)
                return PostSchema.model_validate(updated, from_attributes=True)
        except (DomainPostNotFoundException, DomainCategoryNotFoundException, DomainLocationNotFoundException) as e:
            raise e
        except DatabaseOperationException as e:
            logger.error(e.get_detail())
            raise
