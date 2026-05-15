from src.domain.user.use_cases.user_use_cases import UserUseCases
from src.domain.post.use_cases.post_use_cases import PostUseCases
from src.domain.comment.use_cases.comment_use_cases import CommentUseCases
from src.domain.category.use_cases.category_use_cases import CategoryUseCases
from src.domain.location.use_cases.location_use_cases import LocationUseCases
from src.domain.post.use_cases.get_posts import GetPostsUseCase
from src.domain.post.use_cases.get_post import GetPostUseCase
from src.domain.post.use_cases.get_post_by_id import GetPostByIdUseCase
from src.domain.post.use_cases.create_post import CreatePostUseCase
from src.domain.post.use_cases.update_post import UpdatePostUseCase
from src.domain.post.use_cases.delete_post import DeletePostUseCase


def get_user_use_cases():
    return UserUseCases()


def get_post_use_cases():
    return PostUseCases()


def get_comment_use_cases():
    return CommentUseCases()


def get_category_use_cases():
    return CategoryUseCases()


def get_location_use_cases():
    return LocationUseCases()


def get_get_posts_use_case():
    return GetPostsUseCase()


def get_get_post_use_case():
    return GetPostUseCase()


def get_get_post_by_id_use_case():
    return GetPostByIdUseCase()


def get_create_post_use_case():
    return CreatePostUseCase()


def get_update_post_use_case():
    return UpdatePostUseCase()


def get_delete_post_use_case():
    return DeletePostUseCase()
