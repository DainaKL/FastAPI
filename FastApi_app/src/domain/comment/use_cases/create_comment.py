from src.core.logger import logger

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comment_repository import CommentRepository
from src.infrastructure.sqlite.repositories.post_repository import PostRepository
from src.schemas.comments import Comment as CommentSchema, CommentCreate
from src.core.exceptions.database_exceptions import DatabaseOperationException
from src.core.exceptions.domain_exceptions import PostNotFoundException


class CreateCommentUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = CommentRepository()
        self._post_repo = PostRepository()

    async def execute(self, comment_data: CommentCreate) -> CommentSchema:
        try:
            with self._database.session() as session:
                post = self._post_repo.get_by_id(
                    session=session, post_id=comment_data.post_id
                )
                if not post:
                    error = PostNotFoundException(post_id=comment_data.post_id)
                    logger.error(error.get_detail())
                    raise error

                comment = self._repo.create(session=session, comment=comment_data)
                return CommentSchema.model_validate(comment, from_attributes=True)
        except PostNotFoundException as e:
            raise e
        except DatabaseOperationException as e:
            logger.error(e.get_detail())
            raise
