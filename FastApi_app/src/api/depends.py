from src.domain.category.use_cases.category_use_cases import CategoryUseCases
from src.domain.comment.use_cases.comment_use_cases import CommentUseCases
from src.domain.location.use_cases.location_use_cases import LocationUseCases
from src.domain.post.use_cases.post_use_cases import PostUseCases
from src.domain.user.use_cases.user_use_cases import UserUseCases


def get_user_use_cases() -> UserUseCases:
    return UserUseCases()


def get_post_use_cases() -> PostUseCases:
    return PostUseCases()


def get_comment_use_cases() -> CommentUseCases:
    return CommentUseCases()


def get_category_use_cases() -> CategoryUseCases:
    return CategoryUseCases()


def get_location_use_cases() -> LocationUseCases:
    return LocationUseCases()
