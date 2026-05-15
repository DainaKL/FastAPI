def get_user_use_cases():
    from src.domain.user.use_cases.user_use_cases import UserUseCases

    return UserUseCases()


def get_post_use_cases():
    from src.domain.post.use_cases.post_use_cases import PostUseCases

    return PostUseCases()


def get_comment_use_cases():
    from src.domain.comment.use_cases.comment_use_cases import CommentUseCases

    return CommentUseCases()


def get_category_use_cases():
    from src.domain.category.use_cases.category_use_cases import CategoryUseCases

    return CategoryUseCases()


def get_location_use_cases():
    from src.domain.location.use_cases.location_use_cases import LocationUseCases

    return LocationUseCases()


def get_get_posts_use_case():
    from src.domain.post.use_cases.get_posts import GetPostsUseCase

    return GetPostsUseCase()


def get_get_post_use_case():
    from src.domain.post.use_cases.get_post import GetPostUseCase

    return GetPostUseCase()


def get_create_post_use_case():
    from src.domain.post.use_cases.create_post import CreatePostUseCase

    return CreatePostUseCase()


def get_update_post_use_case():
    from src.domain.post.use_cases.update_post import UpdatePostUseCase

    return UpdatePostUseCase()


def get_delete_post_use_case():
    from src.domain.post.use_cases.delete_post import DeletePostUseCase

    return DeletePostUseCase()
