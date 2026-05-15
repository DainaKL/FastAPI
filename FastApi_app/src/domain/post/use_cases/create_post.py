from src.core.logger import logger

from src.infrastructure.sqlite.database import database
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


class CreatePostUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = PostRepository()
        self._category_repo = CategoryRepository()
        self._location_repo = LocationRepository()

    async def execute(self, post_data: PostCreate) -> PostSchema:
        try:
            with self._database.session() as session:
                if post_data.category_id is not None:
                    category = self._category_repo.get_by_id(
                        session=session, category_id=post_data.category_id
                    )
                    if not category:
                        error = CategoryNotFoundException(
                            category_id=post_data.category_id
                        )
                        logger.error(error.get_detail())
                        raise error

                if post_data.location_id is not None:
                    location = self._location_repo.get_by_id(
                        session=session, location_id=post_data.location_id
                    )
                    if not location:
                        error = LocationNotFoundException(
                            location_id=post_data.location_id
                        )
                        logger.error(error.get_detail())
                        raise error

                post = self._repo.create(session=session, post=post_data)
                return PostSchema.model_validate(post, from_attributes=True)
        except (CategoryNotFoundException, LocationNotFoundException) as e:
            raise e
        except DatabaseOperationException as e:
            logger.error(e.get_detail())
            raise
