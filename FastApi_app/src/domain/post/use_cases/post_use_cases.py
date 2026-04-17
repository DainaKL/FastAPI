from src.domain.post.use_cases.get_posts import GetPostsUseCase
from src.domain.post.use_cases.get_post import GetPostUseCase
from src.domain.post.use_cases.create_post import CreatePostUseCase
from src.domain.post.use_cases.update_post import UpdatePostUseCase
from src.domain.post.use_cases.delete_post import DeletePostUseCase


class PostUseCases:
    def __init__(self):
        self.get_all = GetPostsUseCase().execute
        self.get_by_id = GetPostUseCase().execute
        self.create = CreatePostUseCase().execute
        self.update = UpdatePostUseCase().execute
        self.delete = DeletePostUseCase().execute
