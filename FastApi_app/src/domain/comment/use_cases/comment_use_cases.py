from src.domain.comment.use_cases.get_comments import GetCommentsUseCase
from src.domain.comment.use_cases.get_published_comments import (
    GetPublishedCommentsUseCase,
)
from src.domain.comment.use_cases.get_comment import GetCommentUseCase
from src.domain.comment.use_cases.get_comments_by_post import GetCommentsByPostUseCase
from src.domain.comment.use_cases.get_comments_by_author import (
    GetCommentsByAuthorUseCase,
)
from src.domain.comment.use_cases.create_comment import CreateCommentUseCase
from src.domain.comment.use_cases.update_comment import UpdateCommentUseCase
from src.domain.comment.use_cases.delete_comment import DeleteCommentUseCase


class CommentUseCases:
    def __init__(self):
        self.get_all = GetCommentsUseCase().execute
        self.get_published = GetPublishedCommentsUseCase().execute
        self.get_by_id = GetCommentUseCase().execute
        self.get_by_post = GetCommentsByPostUseCase().execute
        self.get_by_author = GetCommentsByAuthorUseCase().execute
        self.create = CreateCommentUseCase().execute
        self.update = UpdateCommentUseCase().execute
        self.delete = DeleteCommentUseCase().execute
