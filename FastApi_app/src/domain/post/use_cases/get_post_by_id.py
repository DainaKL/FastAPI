from src.core.logger import logger
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post_repository import PostRepository
from src.schemas.posts import Post as PostSchema
from src.core.exceptions.database_exceptions import DatabaseOperationException
from src.core.exceptions.domain_exceptions import PostNotFoundException


class GetPostByIdUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> PostSchema:
        try:
            with self._database.session() as session:
                post = self._repo.get_by_id(session=session, post_id=post_id)
                if not post:
                    raise PostNotFoundException(post_id=post_id)
                return PostSchema.model_validate(post, from_attributes=True)
        except PostNotFoundException as e:
            raise e
        except DatabaseOperationException as e:
            logger.error(e.get_detail())
            raise
