import logging
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comment_repository import CommentRepository
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.infrastructure.sqlite.repositories.post_repository import PostRepository
from src.schemas.comments import Comment as CommentSchema, CommentCreate
from src.core.exceptions.domain_exceptions import (
    UserNotFoundByLoginException,
    PostNotFoundException,
)

logger = logging.getLogger(__name__)


class CreateCommentUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = CommentRepository()
        self._user_repo = UserRepository()
        self._post_repo = PostRepository()

    async def execute(self, data: CommentCreate) -> CommentSchema:
        with self._database.session() as session:
            user = self._user_repo.get_by_id(session=session, user_id=data.author_id)
            if not user:
                raise UserNotFoundByLoginException(login=str(data.author_id))

            post = self._post_repo.get_by_id(session=session, post_id=data.post_id)
            if not post:
                raise PostNotFoundException(post_id=data.post_id)

            comment = self._repo.create(session=session, comment=data)
            return CommentSchema.model_validate(comment, from_attributes=True)
